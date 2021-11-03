from functools import reduce

class Orquestrator():

    def __init__(self):

        self.validators = []
        self.operator   = lambda x,y : x and y

    def addValidator(self, validator):

        self.validators.append(validator)

    def overwriteOperator(self, operator):
        
        self.operator = operator
    
    def cleanValidators(self):

        self.validators.clear()

    def validate(self, transaction):

        return reduce(self.operator, [ val.validate(transaction) for val in self.validators ])
