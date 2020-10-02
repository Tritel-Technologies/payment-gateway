from gateway.models import *
from gateway import create_app, db
from gateway.models import TransactionHeader, TransactionLine, MpesaTransaction
from gateway.saf_end_points.saf_methods import SafMethods
import uuid


class Logic:

    def __init__(self):
        pass

    def make_payment(self, pay_load):
        if 'member_number' in pay_load:
            unique_id = uuid.uuid1()
            unique_id = str(unique_id)[:6]
            tx_ref = unique_id+pay_load['member_number']
            lines = [TransactionLine(
                amount=100, transaction_type='deposit') for x in pay_load['lines']]
            transaction = MpesaTransaction(uiid=tx_ref)
            transaction_header = TransactionHeader(
                transaction_type='paybill', uiid=tx_ref, transaction_line=lines, mpesa_transaction=transaction)
            db.session.add(transaction_header)
            db.session.commit()
            with SafMethods() as payments:
                response = payments.send_push(
                    args=pay_load['lines'], phone_number=pay_load['phone'],
                    member_number=pay_load['member_number'], uiid=tx_ref)

        else:
            print("No")

    
