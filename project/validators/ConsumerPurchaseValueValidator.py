from project.spark_validator import ValidatorTask
from pyspark.sql.functions import col,when,count,min,max,mean,stddev

class ConsumerPurchaseValueValidator(ValidatorTask):

    def __init__(self, spark=None, min_purchases=4, multiplier=2):

        self.min_purchases = min_purchases
        self.multiplier    = multiplier

        super().__init__(spark)
        
        self._build_tmp_view()

    def _build_tmp_view(self):

        df = self._get_transactions() 
		
        df_p_values = df.filter(~col('has_cbk'))\
                .groupBy('user_id')\
                .agg(
                    count('transaction_amount').alias('count'),
                    min('transaction_amount').alias('min'),
                    max('transaction_amount').alias('max'),
                    mean('transaction_amount').alias('avg'), 
                    stddev('transaction_amount').alias('stddev'))\
                .filter(~col('stddev').isNull())\
                .sort(col('avg').desc(), col('stddev').desc())\
                .withColumn('avg', col('avg').cast('decimal(12,2)'))\
                .withColumn('stddev', col('stddev').cast('decimal(12,2)'))

        df.join(df_p_values, 'user_id', 'left')\
          .createTempView('vw_user_value')

    def validate(self, transaction):

        query  = 'SELECT * FROM vw_user_value WHERE user_id = %s AND count > %d AND transaction_amount > %d * (avg + stddev)'
        result = self.spark.sql(query % (transaction['user_id'], self.min_purchases, self.multiplier)).collect()

        if not result:
            return True

        return False
