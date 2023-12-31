import base64
import hashlib
import json
from enum import Enum

import requests

PAYMENT_KEY = 'qi9xF6olbFUPKocZGlTX2C00tEhG8vMtYq20OYebgLNRnkrG1bWBrnU38TczInEcVhjg3gnqpcO2zSsCqjghCpiruTh9hhRaPxDlc0ezXf3k7fKw6EhAxzYWIITA1KFr'
MERCHANT_UUID = '6418cf15-2c59-4d98-8e56-8ffa493471b4'
URL_CALLBACK = 'http://89.223.122.136:8001/'


class AllowedCurrencies(Enum):
    AVAX = 'AVAX'
    BNB = 'BNB'
    BTC = 'BTC'
    BUSD = 'BUSD'
    ETH = 'ETH'
    LTC = 'LTC'
    MATIC = 'MATIC'
    SOL = 'SOL'
    TON = 'TON'
    USDC = 'USDC'
    USDT = 'USDT'


def create_payment(order_id: str, amount: float, to_currency: str):
    data = {
        'amount': str(amount),
        'currency': 'USD',
        'order_id': order_id,
        'url_callback': URL_CALLBACK,
        'is_payment_multiple': True,
        'lifetime': '10800',
        'to_currency': to_currency
    }
    body_data, sign = crypt_data(data)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "merchant": MERCHANT_UUID,
        "sign": sign
    }
    r = requests.post('https://api.cryptomus.com/v1/payment', data=body_data, headers=headers)
    return r.json()


def test_webhook(order_id: str):
    data = {
        'url_callback': URL_CALLBACK,
        'currency': 'USDT',
        'network': 'eth',
        'order_id': order_id,
        'status': 'paid'
    }
    body_data, sign = crypt_data(data)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "merchant": MERCHANT_UUID,
        "sign": sign
    }
    requests.post('https://api.cryptomus.com/v1/test-webhook/payment', data=body_data, headers=headers)


def crypt_data(data):
    json_body_data = json.dumps(data, separators=(',', ':'))
    json_body_data_binary = json_body_data.encode('utf-8')
    encoded_data = base64.b64encode(json_body_data_binary)
    sign_md5_obj = hashlib.md5(encoded_data + PAYMENT_KEY.encode('utf-8'))
    return json_body_data, sign_md5_obj.hexdigest()


# test_webhook('b7bf1364-514a-45ff-98e9-fffaa868dcd5')
