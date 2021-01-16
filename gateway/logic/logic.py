from gateway.models import *
from gateway import create_app, db
from gateway.models import TransactionHeader, TransactionLine, MpesaTransaction
from gateway.saf_end_points.saf_methods import SafMethods
import uuid
import jsonrpclib

HOST = '45.77.141.173'
PORT = 9069
DB = 'autolampstraining'
USER = 'admin'
PASS = 'admin'
ROOT = "http://%s:%s/jsonrpc" % (HOST, PORT)


class Logic:

    def __init__(self):
        self.server = jsonrpclib.ServerProxy(ROOT)
        self.uid = self.server.call(
            service="common", method="login", args=[DB, USER, PASS])

    def invoke(self, model, method, *args):
        args = [DB, self.uid, PASS, model, method] + list(args)
        return self.server.call(service="object", method="execute", args=args)

    def invoke_workflow(self, model, method, *args):
        args = [DB, self.uid, PASS, model, method] + list(args)
        return self.server.call(
            service="object",
            method="exec_workflow",
            args=args)

    def make_payment(self, pay_load):
        if 'member_number' in pay_load:
            unique_id = uuid.uuid1()
            unique_id = str(unique_id)[:6]
            tx_ref = unique_id+pay_load['member_number']
            lines = [TransactionLine(
                amount=x['amount'],
                transaction_type=x['transaction_type'],
                loan_id=x['loan_id'] if 'loan_id' in x else None) for x in pay_load['lines']]
            transaction = MpesaTransaction(uiid=tx_ref)
            transaction_header = TransactionHeader(
                transaction_type=pay_load['header']['transaction_type'],
                uiid=tx_ref, transaction_line=lines, mpesa_transaction=transaction)
            db.session.add(transaction_header)
            db.session.commit()
            with SafMethods() as payments:
                response = payments.send_push(
                    args=pay_load['lines'], phone_number=pay_load['phone'],
                    member_number=pay_load['member_number'], uiid=tx_ref)
                return response

        else:
            return "No member"

    def get_tx(self, tx_ref):
        transaction = TransactionHeader.query.filter(
            TransactionHeader.uiid == tx_ref).first()
        transactionHeader_schema = TransactionHeaderSchema()
        data = transactionHeader_schema.dump(transaction)
        return data

    def post_to_odoo(self, payload):
        try:
            self.invoke('mpesa.payment.transaction',
                        'create', [{'name': payload['BillRefNumber'],
                                    'customer_name':f"{payload['FirstName']} {payload['LastName']}",
                                    "amount":payload['TransAmount'],
                                    'phone_number':payload['MSISDN'],
                                    "reference":payload['InvoiceNumber'],
                                    "payment_date":datetime.strftime(payload['TransTime'], '%Y%m%d%H%M%S')}])
        except Exception as e:
            print(e)
