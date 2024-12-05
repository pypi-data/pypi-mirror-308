from typing import List
from pyspark.sql import DataFrame as SparkDataFrame, SparkSession
from schemon_python_logger.decorator import log_method
from schemon.notebook.base import Section, Store
from schemon_python_logger.logger import Logger
from schemon.notebook.base.platform_manager import PlatformManager
from schemon.notebook.engine.spark.spark_section_config import SparkSectionConfig
from schemon.domain.contract.contract import Contract
from schemon_python_logger.print import print_df as print_df_logger
from schemon.service.notebook.base.store_service import (
    append_or_update_store,
    get_store,
)
from schemon.service.notebook.spark.spark_platform_manager_service import (
    extract_incremental_kwarg,
)


class SparkSection(Section):
    def __init__(
        self,
        spark: SparkSession,
        config: SparkSectionConfig = None,
        logger: Logger = None,
    ):
        name = config.name
        use_thread_pool = config.use_thread_pool
        use_process_pool = config.use_process_pool
        use_spark_rdd = config.use_spark_rdd
        max_workers = config.max_workers
        self.config: SparkSectionConfig = config
        self.stores: List[Store] = []
        super().__init__(
            name,
            spark,
            use_thread_pool,
            use_process_pool,
            use_spark_rdd,
            max_workers,
            logger,
        )

    def set_section_config(self, config: SparkSectionConfig):
        self.config = config
        super().set_name(config.name)
        super().set_executor_manager(
            config.use_thread_pool,
            config.use_process_pool,
            config.use_process_pool,
            self.spark,
        )

    @log_method
    def cleanup(self, contract: Contract):
        stage = contract.stage
        entity_name = contract.entity.name
        entities = [store.contract.entity.name for store in self.stores]
        self.logger.debug(
            f"entities before cleanup: {entities}",
            stage,
            entity_name,
        )
        stores_to_remove = []
        for store in self.stores:
            if store.contract == contract:
                if isinstance(store.df, SparkDataFrame) and store.df is not None:
                    storage_level = store.df.rdd.getStorageLevel()
                    if storage_level.useMemory or storage_level.useDisk:
                        store.df.unpersist()
                    store.df = None
                stores_to_remove.append(store)

        entities_to_remove = [store.contract.entity.name for store in stores_to_remove]
        self.logger.debug(
            f"entities to be removed: {entities_to_remove}",
            stage,
            entity_name,
        )

        self.stores = [store for store in self.stores if store not in stores_to_remove]
        entities_remaining = [store.contract.entity.name for store in self.stores]
        self.logger.debug(
            f"entities remained: {entities_remaining}",
            stage,
            entity_name,
        )

    @log_method
    def truncate(self, contract: Contract):
        target_platform_manager = self.config.target_platform_manager
        target_platform_manager.truncate(contract)

    @log_method
    def read(self, contract: Contract):
        stage = contract.stage
        entity_name = contract.entity.name
        source_platform_manager = self.config.source_platform_manager
        target_platform_manager = self.config.target_platform_manager
        platform = target_platform_manager.platform
        database = target_platform_manager.database
        schema = target_platform_manager.schema
        table = (
            target_platform_manager.table
            if target_platform_manager.table
            else contract.entity.name
        )
        kwarg: dict = None

        if not self.config.source_platform_manager:
            self.logger.error(
                "read() - source_platform_manager is not set.",
                stage,
                entity_name,
            )
            raise ValueError("source_platform_manager is not set.")

        if hasattr(source_platform_manager, "incremental"):
            try:
                incremental = (
                    source_platform_manager.incremental
                    if source_platform_manager.incremental != ""
                    else None
                )
                kwarg = extract_incremental_kwarg(
                    self.spark,
                    platform,
                    contract,
                    incremental,
                    database,
                    schema,
                    table,
                    target_platform_manager.client,
                )
                self.logger.info(
                    f"read() - kwarg value: {kwarg}",
                    stage,
                    entity_name,
                )
            except KeyError as e:
                self.logger.error(
                    "read() - Query formatting error: Missing key {e}",
                    stage,
                    entity_name,
                )
                raise ValueError(
                    contract.entity.name, f"Query formatting error: Missing key {e}"
                )

        df = source_platform_manager.read(contract, kwarg)
        store = Store(contract, df)
        append_or_update_store(self.stores, store)
        print_df(source_platform_manager, df)

    @log_method
    def transform(self, contract: Contract):
        store: Store = get_store(self.stores, contract)
        if store.df.count() == 0:
            return store.df
        target_platform_manager = self.config.target_platform_manager
        df = target_platform_manager.transform(store.df, contract)
        store.df = df

        print_df(target_platform_manager, df)

    @log_method
    def write(self, contract: Contract):
        store: Store = get_store(self.stores, contract)
        if store.df.count() == 0:
            return
        target_platform_manager = self.config.target_platform_manager
        df = target_platform_manager.write(store.df, contract)

        print_df(target_platform_manager, df)

    def run(self, contract: Contract):
        if contract.config.transformation_config.truncate:
            self.truncate(contract)
        self.read(contract)
        self.transform(contract)
        self.write(contract)
        self.cleanup(contract)


def print_df(platform_manager: PlatformManager, df):
    if platform_manager.show_data:
        n = platform_manager.show_data.get("n", 20)
        vertical = platform_manager.show_data.get("vertical", False)
        truncate = platform_manager.show_data.get("truncate", True)
        print_df_logger(df, n, vertical, truncate)
