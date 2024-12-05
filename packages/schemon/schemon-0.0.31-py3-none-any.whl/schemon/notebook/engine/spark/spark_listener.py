import os
from pyspark.sql import SparkSession, DataFrame
from schemon.domain.base import Base


class SchemonSparkListner(Base):
    def __init__(
        self,
        spark: SparkSession,
    ):
        self.spark = spark
        self.add_listener()

    def add_listener(self):
        context = self.spark.sparkContext
        # TODO: Fix this
        # Databricks throws an error when trying to create a listener
        self.listener = context._jvm.com.schemon.app.SchemonSparkListener()
        context._jsc.sc().addSparkListener(self.listener)

    def write_to_local(self, output_dir: str = None, mode: str = "append"):
        if output_dir is None:
            output_dir = f"{os.getcwd()}/metrics"
        self.listener.writeToParquet(self.spark._jsparkSession, output_dir, mode)

    def write_to_s3(self, mode: str = "append"):
        bucket_path = "s3a://schemon-event-log"
        event_dfs = self.listener.createEventDataFrames(self.spark._jsparkSession)

        job_df_java = event_dfs.getJobDF()
        job_df = DataFrame(job_df_java, self.spark)
        job_df.coalesce(1).write.mode(mode).parquet(f"{bucket_path}/jobs")

        stage_df_java = event_dfs.getStageDF()
        stage_df = DataFrame(stage_df_java, self.spark)
        stage_df.coalesce(1).write.mode(mode).parquet(f"{bucket_path}/stages")

        task_df_java = event_dfs.getTaskDF()
        task_df = DataFrame(task_df_java, self.spark)
        task_df.coalesce(1).write.mode(mode).parquet(f"{bucket_path}/tasks")

        executor_df_java = event_dfs.getExecutorDF()
        executor_df = DataFrame(executor_df_java, self.spark)
        executor_df.coalesce(1).write.mode(mode).parquet(f"{bucket_path}/executors")


if __name__ == "__main__":
    # Initialize SparkSession
    spark = (
        SparkSession.builder.appName("ListenerExample")
        .config(
            "spark.jars",
            "/home/onword/repo/schemoninc/spark-listener/target/spark-listener-1.0-SNAPSHOT.jar",
        )
        .config("spark.extraListeners", "com.schemon.app.SchemonSparkListener")
        .getOrCreate()
    )

    listener = SchemonSparkListner(spark)
    # Run your Spark job
    df = spark.range(10000)
    df = df.withColumn("square", df["id"] * df["id"])
    df.show()

    # Call the writeToParquet method after job completion
    listener.write()

    # Stop Spark
    spark.stop()
