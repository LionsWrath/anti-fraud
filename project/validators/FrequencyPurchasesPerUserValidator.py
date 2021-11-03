from project.spark_validator import ValidatorTask
from pyspark.sql.functions import col,when,to_date,count,mean,stddev

class FrequencyPurchasesPerUserValidator(ValidatorTask):

    def __init__(self, spark=None):

        super().__init__(spark)
        
        self._build_tmp_view()

    def _build_tmp_view(self):

        df = self._get_transactions() 

        df_p_purchases = df.withColumn('date', to_date(col('transaction_date')))\
                   .groupBy('user_id', 'date')\
                   .count()\
                   .sort(col('count').desc())

# Calculate the mean and deviation for each consumer
# Null standard deviation is removed because is trivial
        df_p_purchases_agg = df_p_purchases.groupBy('user_id')\
                                   .agg(
                                        count('count').alias('count'),
                                        mean('count').alias('avg'), 
                                        stddev('count').alias('stddev'))\
                                   .sort(col('avg').desc(), col('stddev').desc())\
                                   .withColumn('avg', col('avg').cast('decimal(12,2)'))\
                                   .withColumn('stddev', col('stddev').cast('decimal(12,2)'))\
                                   .createTempView('vw_user_purchases_agg')

    def validate(self, transaction):

        query  = 'SELECT * FROM vw_user_purchases_agg WHERE ROUND(avg + stddev, 2) > %f AND user_id = %d'
        result = self.spark.sql(query % (transaction['transaction_amount'], transaction['user_id'])).collect()

        if not result:
            return True

        return not result[0]['is_suspicious']
