from flask import Blueprint, request, json, current_app
from gateway import db
from gateway.logic.logic import Logic
from flask import jsonify
from gateway.models import MpesaTransaction
from logging.handlers import SMTPHandler, RotatingFileHandler
import logging
from datetime import datetime
import requests

mod = Blueprint('api', __name__, url_prefix='/api')


@mod.route('/payment', methods=['POST'],)
def make_payment():
    data = request.json
    print(request.json['header'])
    logic = Logic()
    response = logic.make_payment(data)
    return response


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
    tx_ref = request.json['BillRefNumber']
    datetime_str = request.json['TransTime']
    datetime_object = datetime.strptime(datetime_str, '%Y%m%d%H%M%S')
    transaction = MpesaTransaction.query.filter(
        MpesaTransaction.uiid == tx_ref).first()

    if transaction is not None:
        transaction.transaction_type = request.json['TransactionType']
        transaction.transaction_id = request.json['TransID']
        transaction.transaction_time = datetime_object
        transaction.trasnction_amount = request.json['TransAmount']
        transaction.business_short_code = request.json['BusinessShortCode']
        transaction.msisdn = request.json['MSISDN']
        transaction.first_name = request.json['FirstName']
        db.session.add(transaction)
        db.session.commit()
        logic = Logic()
        data = logic.get_tx(tx_ref)
        print(data)
        api_url = "https://api-sacco.tritel.co.ke/api/postPayment"
        response = requests.post(
            api_url, json=data)

    else:

        transaction = MpesaTransaction(
            bill_ref=request.json['BillRefNumber'], 
            uiid=request.json['BillRefNumber'], 
            trasnction_amount=request.json['TransAmount'],
            first_name=request.json['FirstName'])

        db.session.add(transaction)
        db.session.commit()
        data = {"params":request.json}
        odoo_url = 'http://3914bde920d5.ngrok.io/payment/mpesa/callback'
        requests.post(
            odoo_url, json=data)
        # payment = MpesaTransaction(name=request.json['FirstName'], amount=request.json['TransAmount'],
        #                        phone_number=request.json['MSISDN'], bill_ref=request.json['BillRefNumber'],
        #                        transaction_id=request.json['TransID'])
        # with Logic() as logic:
        #     logic.deposit(res['lines'], res)
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return "json(context)"


@mod.route('/getTx', methods=['POST'])
def get_tx():
    logic = Logic()
    return logic.get_tx(request.json['tx'])
