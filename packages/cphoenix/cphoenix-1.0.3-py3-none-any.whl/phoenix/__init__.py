import os
import pathlib
from pyspark.sql import SparkSession
from pyspark.sql.dataframe import DataFrame


CURR_DIR = str(pathlib.Path(__file__).parent.resolve())
JARS = ['iceberg-aws-bundle-1.7.0.jar.py', 'iceberg-spark-runtime-3.5_2.12-1.7.0.jar.py']
PACKAGES = ','.join([os.path.expanduser(CURR_DIR + "/../jars/" + jar) for jar in JARS])

def get_catalog_config(client_id: str, client_secret: str, env: str) -> dict:
    return {
        f'spark.sql.catalog.{env}_nessie': 'org.apache.iceberg.spark.SparkCatalog',
        f'spark.sql.catalog.{env}_nessie.type': 'rest',
        f'spark.sql.catalog.{env}_nessie.s3.path-style-access': 'true',
        f'spark.sql.catalog.{env}_nessie.uri': f'https://{env}-lakehouse-nessie.cads.live/iceberg',
        f'spark.sql.catalog.{env}_nessie.scope': 'catalog sign',
        f'spark.sql.catalog.{env}_nessie.oauth2-server-uri': f'https://{env}-lakehouse.cads.live/keycloak/auth/realms/master/protocol/openid-connect/token',
        f'spark.sql.catalog.{env}_nessie.credential': f'{client_id}:{client_secret}'
    }


class Phoenix:

    def __init__(self, 
                client_id: str,
                client_secret: str,
                env: str = 'staging',
                master: str = 'local'
            ):
        catalog_config = get_catalog_config(client_id, client_secret, env)
        self._spark = (
            SparkSession.builder
            .master(master)
            .config("spark.jars", PACKAGES)
            .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
            .config("spark.sql.defaultCatalog", "staging_nessie")
            .config(map=catalog_config)
            .getOrCreate()
        )

    def get_spark_session(self) -> SparkSession:
        return self._spark

    def sql(self, sqlQuery: str) -> DataFrame:
        return self._spark.sql(sqlQuery)
