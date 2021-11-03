from project.spark_validator import ValidatorTask
from pyspark.sql.functions import col,when

class ConsumerChargebackRateValidator(ValidatorTask):

    def __init__(self, spark=None, min_purchases=3, max_rate=50.0):

        self.min_purchases = min_purchases
        self.max_rate      = max_rate

        super().__init__(spark)
        
        self._build_tmp_view()

    def _build_tmp_view(self):

        df = self._get_transactions() 

        df_p_totals = df.groupBy('user_id')\
                       .count()\
                       .sort(col('count').desc())\
                       .withColumnRenamed('count', 'total_purchases')

        df_p_chargebacks = df.groupBy('user_id', 'has_cbk')\
                             .count()\
                             .orderBy(col('user_id').desc())

        df_p_chargebacks_f = df_p_chargebacks.filter(~col('has_cbk'))\
                                     .select('user_id','count')\
                                     .withColumnRenamed('count', 'sum_f')
        df_p_chargebacks_t = df_p_chargebacks.filter( col('has_cbk'))\
                                     .select('user_id','count')\
                                     .withColumnRenamed('count', 'sum_t')

        # The consumer  chargeback rate is a rate for fraud prone 
        # payment detection based on the number of chargebacks of 
        # the consumer. Maybe a minimum number of purchases is needed
        # to filter stores that are in the beginning.
        df_p_rates = df_p_totals\
                .join(df_p_chargebacks_f, 'user_id', 'left')\
                .join(df_p_chargebacks_t, 'user_id', 'left')\
                .withColumn('sum_f', when(col('sum_f').isNull(), 0).otherwise(col('sum_f')))\
                .withColumn('sum_t', when(col('sum_t').isNull(), 0).otherwise(col('sum_t')))\
                .withColumn('rate', ((col('sum_t') * 100) / col('total_purchases')).cast('decimal(10,2)') )\
                .orderBy(col('rate').desc())\
                .withColumn('is_suspicious', when((col('rate') > self.max_rate) & (col('total_purchases') > self.min_purchases), True).otherwise(False))\
                .createTempView('vw_consumer_cbk_rate')

    def validate(self, transaction):

        query  = 'SELECT user_id,is_suspicious FROM vw_consumer_cbk_rate WHERE user_id = %s'
        result = self.spark.sql(query % transaction['user_id']).collect()

        if not result:
            return True

        return not result[0]['is_suspicious']
