import os
import tempfile
from pyspark.sql import SparkSession

class ConfigError(ValueError):
    """Custom exception for configuration errors."""
    pass

class Config:
    """
    Configuration class for database connection settings.
    Supported engines:
    - sqlite3
    - mysql
    - databricks
    """

    def __init__(self):
        self.db_type = self._get_env_variable("DB_TYPE")
        self.database_uri = None
        self.connect_args = {}
        self.show_sql = os.getenv("SHOW_SQL") == "1"
        
        self._configure_database()

    def _get_env_variable(self, var_name, required=True, default=None):
        """Helper method to retrieve environment variables with error handling."""
        value = os.getenv(var_name, default)
        if required and value is None:
            raise ConfigError(f"Environment variable '{var_name}' is required.")
        return value

    def _configure_database(self):
        """Configure database settings based on DB_TYPE."""
        if self.db_type == "sqlite3":
            self.database_uri = self._get_env_variable("DATABASE_URL")
        
        elif self.db_type == "mysql":
            mysql_password = self._get_env_variable("MYSQL_PASSWORD")
            mysql_url = self._get_env_variable("DATABASE_URL")
            self.database_uri = mysql_url.format(MYSQL_PASSWORD=mysql_password)
            if "DATABASE_CERTIFICATE_PATH" in os.environ:
                self.connect_args = {
                    'ssl_ca': self._get_env_variable("DATABASE_CERTIFICATE_PATH")
                }
            elif "DATABASE_CERTIFICATE_DB" in os.environ:
                # It works only when the data is stored in a hive table or maybe other db with two namespaces.
                # It is meant to ease up the pain using Databricks Community edition so the engine can interact with the external mysql database,
                # requires the certificate.
                query = self._get_env_variable("DATABASE_CERTIFICATE_DB")
                cert_df = spark.sql(query)  # type: ignore
                ca_cert = cert_df.collect()[0]["value"]

                # Save the CA certificate to a temporary file
                with tempfile.NamedTemporaryFile(suffix=".pem", delete=True) as temp_cert_file:
                    temp_cert_file.write(ca_cert.encode())
                    temp_cert_path = temp_cert_file.name
                self.connect_args = {
                    'ssl': temp_cert_path
                }
        
        elif self.db_type == "databricks":
            self._configure_databricks()

        else:
            raise ConfigError(f"DB_TYPE '{self.db_type}' is not supported. Supported types: sqlite3, mysql, databricks")

    def _configure_databricks(self):
        """Configure Databricks-specific settings."""
        access_token = self._get_env_variable("DATABRICKS_TOKEN")
        server_hostname = self._get_env_variable("DATABRICKS_SERVER_HOSTNAME")
        sql_warehouse_http_path = self._get_env_variable("DATABRICKS_SQL_WAREHOUSE_HTTP_PATH")
        catalog = self._get_env_variable("DATABRICKS_CATALOG")
        schema = self._get_env_variable("DATABRICKS_SCHEMA")

        self.database_uri = (
            f"databricks://token:{access_token}@{server_hostname}"
            f"?http_path={sql_warehouse_http_path}&catalog={catalog}&schema={schema}"
        )
        self.connect_args = {"_tls_verify_hostname": True}


# Use the Config class to retrieve settings
try:
    config = Config()
    # Access config attributes as needed
except ConfigError as e:
    print(f"Configuration Error: {e}")
    exit(1)
    # Handle or exit depending on your requirements
