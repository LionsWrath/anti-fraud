import argparse
from functools import reduce
from project.api import AntiFraudAPI, APIWrapper
from project.orchestrator import Orquestrator
from project.validators.MerchantChargebackRateValidator import MerchantChargebackRateValidator
from project.validators.ConsumerChargebackRateValidator import ConsumerChargebackRateValidator
from project.validators.FrequencyPurchasesPerUserValidator import FrequencyPurchasesPerUserValidator
from project.validators.MerchantPurchaseValueValidator import MerchantPurchaseValueValidator
from project.validators.ConsumerPurchaseValueValidator import ConsumerPurchaseValueValidator
from project.validators.TransactionDeviceValidator import TransactionDeviceValidator

parser = argparse.ArgumentParser(description='Anti-fraud System for Transaction Validation')

parser.add_argument('-p', '--profile', dest='p',  choices=['base', 'over', 'all'], default='base', help='Validator profile')
parser.add_argument('-o', '--operator', dest='o',  choices=['soft', 'tight'], default='tight', help='Operator profile')
parser.add_argument('-r', '--add-results', dest='r', action='store_true', help="Add results to response")

if __name__ == '__main__':
    system = APIWrapper('cloudwalk')

    # Build Orquestrator
    orc   = Orquestrator()
    cargs = parser.parse_args()

    # Add Validators
    if cargs.p == 'all':

        orc.addValidator('merchant_cbk_rate', MerchantChargebackRateValidator())
        orc.addValidator('consumer_cbk_rate', ConsumerChargebackRateValidator())
        orc.addValidator('frequency_purchase_user', FrequencyPurchasesPerUserValidator())
        orc.addValidator('merchant_purchase_val', MerchantPurchaseValueValidator())
        orc.addValidator('consumer_purchase_val', ConsumerPurchaseValueValidator())
        orc.addValidator('transaction_device', TransactionDeviceValidator())

    elif cargs.p == 'base':
        
        orc.addValidator('merchant_purchase_val', MerchantPurchaseValueValidator())
        orc.addValidator('consumer_purchase_val', ConsumerPurchaseValueValidator())
        orc.addValidator('transaction_device', TransactionDeviceValidator())

    elif cargs.p == 'over':

        orc.addValidator('merchant_cbk_rate', MerchantChargebackRateValidator())
        orc.addValidator('consumer_cbk_rate', ConsumerChargebackRateValidator())

    if cargs.o == 'soft':

        orc.overwriteOperator(lambda x : reduce(lambda a,b : a or b, x.values()))

    system.add_endpoint(AntiFraudAPI, '/transaction-validation', resource_class_kwargs={
        'orchestrator' : orc, 
        'add_results'  : True if cargs.r else False
    })

    system.run()
    

