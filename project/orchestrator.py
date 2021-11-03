from functools import reduce

class Orquestrator():

    def __init__(self):

        self.validators = {}
        self.operator   = lambda x : reduce(lambda a,b : a and b, x.values()) 

    def addValidator(self, name, validator):

        self.validators[name] = validator

    def overwriteOperator(self, operator):
        
        self.operator = operator
    
    def cleanValidators(self):

        self.validators.clear()

    def validate(self, transaction):
        
        self._call_validators(transaction)

        return self.operator(self.results)

    def _call_validators(self, transaction):

        self.results = { key : val.validate(transaction) for key,val in self.validators.items() }

    def get_results(self):
        
        return self.results
