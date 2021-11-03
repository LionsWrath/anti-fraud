from pyspark.sql import SparkSession
from abc import ABC, abstractmethod
from logging import Logger
import os

class ValidatorTask():

    def __init__(self, spark=None):

        self.spark  =  self._prepare_spark(spark)
        self.logger =  self._prepare_logger()

        self.name   = ''
        self.tables = {
                'transactions' : os.path.join(os.getcwd(), 'spark-warehouse/tb_transactions.delta')
        }

    def _get_transactions(self):
        return self.spark.read\
                    .format('delta')\
                    .load(self.tables['transactions'])

    @staticmethod
    def _prepare_spark(spark) -> SparkSession:
        if not spark:
            return SparkSession.builder\
                    .config("spark.jars.packages", "io.delta:delta-core_2.12:1.0.0")\
                    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
                    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")\
                    .appName("TransactionValidation")\
                    .getOrCreate()
        else:
            return spark 

    def _prepare_logger(self) -> Logger:
        log4j_logger = self.spark._jvm.org.apache.log4j # noqa
        return log4j_logger.LogManager.getLogger(self.__class__.__name__)

    @abstractmethod
    def validate(self, transaction) -> bool:
        pass

