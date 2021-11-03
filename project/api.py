from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from marshmallow import Schema, fields, ValidationError

class TransactionSchema(Schema):
    transaction_id     = fields.Int()
    merchant_id        = fields.Int()
    user_id            = fields.Int()
    card_number        = fields.String()
    transaction_date   = fields.DateTime(format="%Y-%m-%dT%H:%M:%S.%f")
    transaction_amount = fields.Float()
    device_id          = fields.Int(allow_none=True)

class AntiFraudAPI(Resource):

    def __init__(self, **kwargs):

        self.orchestrator = kwargs['orchestrator']

        if 'add_results' in kwargs:
            self.add_results  = kwargs['add_results']
        else:
            self.add_results  = False

        self.transaction_schema = TransactionSchema()

        super(AntiFraudAPI, self).__init__()

    def post(self):
        
        request_data = request.get_json()

        try:
            transaction = self.transaction_schema.load(request_data)
        except ValidationError as err:
            return make_response(jsonify(err.messages), 400)

        if self.add_results:
            return jsonify({ 
                'transaction_id' : transaction['transaction_id'],
                'recommendation' : 'approve' if self.orchestrator.validate(transaction) else 'deny',
                'validators'     : self.orchestrator.get_results()
            })

        return jsonify({ 
            'transaction_id' : transaction['transaction_id'],
            'recommendation' : 'approve' if self.orchestrator.validate(transaction) else 'deny'
        })

class APIWrapper(object):

    def __init__(self, name):
        self.app = Flask(name)
        self.api = Api(self.app)

    def run(self):
        self.app.run()

    def add_endpoint(self, endpoint_class, endpoint_name=None, **kwargs):
        self.api.add_resource(endpoint_class, endpoint_name, **kwargs)
