from typing import Union
from schemon.domain.base import Base
from schemon.notebook.platform_manager.spark.s3_platform_manager import (
    S3PlatformManager,
)
from schemon.notebook.platform_manager.spark.hive_platform_manager import (
    HivePlatformManager,
)
from schemon.notebook.platform_manager.spark.mssql_platform_manager import (
    MSSQLPlatformManager,
)
from schemon.notebook.platform_manager.spark.unity_catalog_platform_manager import (
    UnityCatalogPlatformManager,
)


class SparkSectionConfig(Base):
    def __init__(
        self,
        name: str,
        source_platform_manager: Union[
            HivePlatformManager,
            S3PlatformManager,
            UnityCatalogPlatformManager,
            MSSQLPlatformManager,
        ] = None,
        target_platform_manager: Union[
            HivePlatformManager,
            S3PlatformManager,
            UnityCatalogPlatformManager,
            MSSQLPlatformManager,
        ] = None,
        use_thread_pool: bool = False,
        use_process_pool: bool = False,
        use_spark_rdd: bool = False,
        incremental: str = None,
        max_workers: int = None,
    ):
        self.name = name
        self.source_platform_manager: Union[
            HivePlatformManager,
            S3PlatformManager,
            UnityCatalogPlatformManager,
            MSSQLPlatformManager,
        ] = source_platform_manager
        self.target_platform_manager: Union[
            HivePlatformManager,
            S3PlatformManager,
            UnityCatalogPlatformManager,
            MSSQLPlatformManager,
        ] = target_platform_manager
        self.use_thread_pool: bool = use_thread_pool
        self.use_process_pool: bool = use_process_pool
        self.use_spark_rdd: bool = use_spark_rdd
        self.incremental = incremental
        self.max_workers = max_workers
