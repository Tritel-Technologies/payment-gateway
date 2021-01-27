import requests
import json
from requests.auth import HTTPBasicAuth
from datetime import datetime
import base64


class MpesaC2bCredential:
    consumer_key = 'JCWkwPafHudcGnQ33nZA9yAu7PQ1d5dE'
    consumer_secret = 'jNupt8t0OhHRXEqQ'
    api_URL = 'https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'


class MpesaAccessToken:
    def __init__(self):
        self.r = requests.get(MpesaC2bCredential.api_URL,
                              auth=HTTPBasicAuth(MpesaC2bCredential.consumer_key, MpesaC2bCredential.consumer_secret))
        self.mpesa_access_token = json.loads(self.r.text)
        self.validated_mpesa_access_token = self.mpesa_access_token['access_token']

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None or exc_value is None or traceback is not None:
            return exc_value


class LipanaMpesaPpassword:
    lipa_time = datetime.now().strftime('%Y%m%d%H%M%S')
    Business_short_code = "182754"
    Test_c2b_shortcode = "600775"
    passkey = 'd81fd7a83a09bda9d6a45c5f19a493a133c7f214762637cd2eb28c45120760ac'
    data_to_encode = Business_short_code + passkey + lipa_time
    online_password = base64.b64encode(data_to_encode.encode())
    decode_password = online_password.decode('utf-8')


class PaymentTypes:
    deposits = 1
    share_capital = 2
    loan_application = 3
    loan_payment = 4
