from flask import Blueprint, request, json
from gateway import db
from gateway.logic.logic import Logic
from flask import jsonify
from gateway.models import MpesaTransaction

mod = Blueprint('api', __name__, url_prefix='/api')


@mod.route('/payment', methods=['POST'],)
def make_payment():
    data = request.json
    print(request.json['header'])
    logic = Logic()
    logic.make_payment(data)
    return 'ss'


@mod.route('/addPost')
def add_post():
    return 'post'


@mod.route('/validationResponse', methods=['POST'])
def validation_response():
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return json(context)


@mod.route('/confirmationCallback', methods=['POST'])
def confirmation_callback():
    # payment = MpesaTransaction(name=request.json['FirstName'], amount=request.json['TransAmount'],
    #                        phone_number=request.json['MSISDN'], bill_ref=request.json['BillRefNumber'],
    #                        transaction_id=request.json['TransID'])
    # with Logic() as logic:
    #     logic.deposit(res['lines'], res)
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return json(context)
