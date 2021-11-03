from project.spark_validator import ValidatorTask
from pyspark.sql.functions import col,when,count,min,max,mean,stddev

class MerchantPurchaseValueValidator(ValidatorTask):

    def __init__(self, spark=None, min_purchases=4):

        self.min_purchases = min_purchases

        super().__init__(spark)
        
        self._build_tmp_view()

    def _build_tmp_view(self):

        df = self._get_transactions() 
		
        df_m_values = df.filter(~col('has_cbk'))\
                .groupBy('merchant_id')\
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

        df.join(df_m_values, 'merchant_id', 'left')\
          .createTempView('vw_merchant_value')

    def validate(self, transaction):

        query  = 'SELECT * FROM vw_merchant_value WHERE merchant_id = %s AND count > %d AND transaction_amount > 2 * (avg + stddev)'
        result = self.spark.sql(query % (transaction['merchant_id'], self.min_purchases)).collect()

        if not result:
            return True

        return False
