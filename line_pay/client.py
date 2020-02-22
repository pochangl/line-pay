import json
import base64
import hashlib
import hmac
import requests
import uuid
from urllib.parse import urlencode
from . import online


def get_signature(secret, url, data):
    '''
        authentication nonce and hmac signature
        refer to https://pay.line.me/documents/online_v3_cn.html#api-authentication
    '''
    nonce = str(uuid.uuid1())
    key = secret
    msg = secret + url + data + nonce

    key = bytes(key, 'utf8')
    msg = bytes(msg, 'utf8')

    digest = hmac.digest(key, msg, hashlib.sha256)

    signature = base64.b64encode(digest)
    signature = str(signature, encoding='utf8')

    return dict(
        Authorization=signature,
        Nonce=nonce,
    )


class BaseClient:
    host = ''

    def __init__(self, ChannelId, ChannelSecret, MerchantDeviceProfileId=None):
        'initial with merchant info'

        self.ChannelId = ChannelId
        self.MerchantDeviceProfileId = MerchantDeviceProfileId
        self.ChannelSecret = ChannelSecret
        self.prepare_api()

    def get_headers(self, url, data):
        '''
            authentication headers
            refer to https://pay.line.me/documents/online_v3_en.html#api-authentication
        '''
        signature = get_signature(secret=self.ChannelSecret, url=url, data=data)

        data = {
            'Content-Type': 'application/json',
            'X-LINE-ChannelId': self.ChannelId,
            'X-LINE-Authorization-Nonce': signature['Nonce'],
            'X-LINE-Authorization': signature['Authorization'],
        }

        if self.MerchantDeviceProfileId is not None:
            data['X-LINE-MerchantDeviceProfileId'] = self.MerchantDeviceProfileId
        return data

    def post(self, url, data):
        raw_data = json.dumps(data)
        uri = '{}{}'.format(self.host, url)
        headers = self.get_headers(url=url, data=raw_data)
        return requests.post(url=uri, data=raw_data, headers=headers, json=True).json()

    def get(self, url, data):
        qs = urlencode(data)
        uri = '{}{}'.format(self.host, url)
        headers = self.get_headers(url=url, data=qs)
        return requests.get(url=uri, params=qs, headers=headers).json()

    def prepare_api(self):
        self.request = online.RequestAPI(self)
        self.confirm = online.ConfirmAPI(self)
        self.status = online.StatusAPI(self)


class SandboxClient(BaseClient):
    host = 'https://sandbox-api-pay.line.me'


class Client(BaseClient):
    host = 'https://api-pay.line.me'
