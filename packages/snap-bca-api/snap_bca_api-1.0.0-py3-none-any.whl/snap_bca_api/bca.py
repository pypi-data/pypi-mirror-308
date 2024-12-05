import base64
import random
import requests, datetime, hashlib, hmac, json
from OpenSSL import crypto
from datetime import datetime, timedelta, timezone


class BCA_SNAP():

    def __init__(self, client_id, client_secret, private_key, channel_id, partner_id, host="https://sandbox.bca.co.id", debug=False):
        self.client_id = client_id
        self.client_secret = client_secret
        self.private_key = private_key
        self.channel_id = channel_id
        self.partner_id = partner_id
        self.host = host
        self.debug = debug

    def __getTimestamp(self):
        return datetime.now(timezone(timedelta(hours=7))).isoformat(timespec='seconds')

    def __getRandomInt(self):
        random_number = ''.join([str(random.randint(0, 9)) for _ in range(16)])
        return random_number

    def __getSnapAsymetricSignature(self, timestamp):
        pkey = crypto.load_privatekey(crypto.FILETYPE_PEM, self.private_key)
        data = (self.client_id + "|" + timestamp).encode()
        sign = crypto.sign(pkey, data, "sha256")

        data_base64 = base64.b64encode(sign)
        return data_base64

    def __getSnapSymetricSignature(self, method, path, access_token, timestamp, request_body=''):
        secret = self.client_secret.encode()
        request_body_hash = hashlib.sha256(
            request_body.encode()
        ).hexdigest().lower()

        StringToSign = (
            method + ':' +
            path + ':' +
            access_token + ':' +
            request_body_hash + ':' +
            timestamp
        ).encode()

        signature = hmac.new(secret, StringToSign, digestmod=hashlib.sha512)
        return base64.b64encode(signature.digest()).decode()

    def __getSnapAccessToken(self, timestamp):
        headers = {
            'Content-Type': 'application/json',
            'X-TIMESTAMP': timestamp,
            'X-CLIENT-KEY': self.client_id,
            'X-SIGNATURE': self.__getSnapAsymetricSignature(timestamp)
        }

        payload = {'grantType': 'client_credentials'}
        r = requests.post(self.host + '/openapi/v1.0/access-token/b2b', headers=headers, data=json.dumps(payload))
        return r.json()

    def getBalance(self, account_number, partnerReferenceNo, external_id=""):
        path = '/openapi/v1.0/balance-inquiry'

        if external_id == "":
            external_id = self.__getRandomInt()

        timestamp = self.__getTimestamp()
        accessToken = ""
        getAccessToken = self.__getSnapAccessToken(timestamp)
        if getAccessToken["responseCode"] == "2007300":
            accessToken = getAccessToken["accessToken"]
        else:
            return getAccessToken

        payload = {
            "partnerReferenceNo": partnerReferenceNo,
            "accountNo": account_number,
        }

        data = json.dumps(payload, separators=(',', ':'))
        signature = self.__getSnapSymetricSignature(
            'POST', path, accessToken, timestamp, data
        )

        header = {
            "Content-Type": "application/json",
            "X-PARTNER-ID": self.partner_id,
            "Authorization": "Bearer " + accessToken,
            "X-TIMESTAMP": timestamp,
            "CHANNEL-ID": self.channel_id,
            "X-SIGNATURE": signature,
            "X-EXTERNAL-ID": external_id,
        }

        r = requests.post(self.host + path, headers=header, data=data)
        if self.debug:
            print("---- DEBUG RESPONSE HEADER ----")
            print(r.headers)
            print("---- --------------------- ----")

        return r.content.decode()

    def getStatement(self, account_number, partnerReferenceNo, fromDateTime, toDateTime, external_id=""):
        path = '/openapi/v1.0/bank-statement'

        if external_id == "":
            external_id = self.__getRandomInt()

        timestamp = self.__getTimestamp()
        accessToken = ""
        getAccessToken = self.__getSnapAccessToken(timestamp)
        if getAccessToken["responseCode"] == "2007300":
            accessToken = getAccessToken["accessToken"]
        else:
            return getAccessToken

        payload = {
            "partnerReferenceNo": partnerReferenceNo,
            "accountNo": account_number,
            "fromDateTime": fromDateTime,
            "toDateTime": toDateTime,
        }

        data = json.dumps(payload, separators=(',', ':'))
        signature = self.__getSnapSymetricSignature(
            'POST', path, accessToken, timestamp, data
        )

        header = {
            "Content-Type": "application/json",
            "X-PARTNER-ID": self.partner_id,
            "Authorization": "Bearer " + accessToken,
            "X-TIMESTAMP": timestamp,
            "CHANNEL-ID": self.channel_id,
            "X-SIGNATURE": signature,
            "X-EXTERNAL-ID": external_id,
        }
        r = requests.post(self.host + path, headers=header, data=data)
        if self.debug:
            print("---- DEBUG RESPONSE HEADER ----")
            print(r.headers)
            print("---- --------------------- ----")

        return r.content.decode()
