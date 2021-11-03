import argparse
from project.api import AntiFraudAPI, APIWrapper
from project.orchestrator import Orquestrator
from project.validators.MerchantChargebackRateValidator import MerchantChargebackRateValidator
from project.validators.ConsumerChargebackRateValidator import ConsumerChargebackRateValidator
from project.validators.FrequencyPurchasesPerUserValidator import FrequencyPurchasesPerUserValidator

parser = argparse.ArgumentParser(description='Anti-fraud System for Transaction Validation')

command_group = parser.add_mutually_exclusive_group()
command_group.add_argument('-v','--validators', nargs='+', help='Set custom validators')
command_group.add_argument('-p','--profile', help='Validator profile')

parser.add_argument('-s', '--spark-string', nargs='?', help='Spark string', const='local')

if __name__ == '__main__':
    system = APIWrapper('cloudwalk')

    # Build Orquestrator
    orc = Orquestrator()
    orc.addValidator(MerchantChargebackRateValidator())
    orc.addValidator(ConsumerChargebackRateValidator())
    orc.addValidator(FrequencyPurchasesPerUserValidator())

    system.add_endpoint(AntiFraudAPI, '/transaction-validation', resource_class_kwargs={ 'orchestrator' : orc })

    system.run()
    

