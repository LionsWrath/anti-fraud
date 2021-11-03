from project.spark_validator import ValidatorTask
from pyspark.sql.functions import col,when,count,min,max,mean,stddev

class TransactionDeviceValidator(ValidatorTask):

    def validate(self, transaction):

        if transaction['device_id']:
            return True

        return False
