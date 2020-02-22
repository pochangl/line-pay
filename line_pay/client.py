import json
import base64
import hashlib
import hmac
import requests
import uuid
from urllib.parse import urlencode


def get_signature(secret, url, data):
    '''
        authentication nonce and hmac signature
        refer to https://pay.line.me/documents/online_v3_cn.html#api-authentication
    '''
    nonce = uuid.uuid1()
    key = secret
    msg = secret + url + data + nonce

    key = bytes(key, 'utf8')
    msg = bytes(msg, 'utf8')

    digest_maker = hmac.new(key, msg, hashlib.sha256)

    digest = digest_maker.digest()

    signature = base64.encodestring(digest)

    return dict(
        Authorization=signature,
        AuthorizationNonce=nonce,
    )


class BaseClient:
    def __init__(self, ChannelId, ChannelSecret, MerchantDeviceProfileId=None):
        'initial with merchant info'

        self.ChannelId = ChannelId
        self.MerchantDeviceProfileId = MerchantDeviceProfileId
        self.ChannelSecret = ChannelSecret

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
        headers = self.get_headers(url=url, data=data)
        raw_data = json.dumps(data)
        return requests.post(url=url, data=raw_data, headers=headers, json=True)

    def get(self, url, data):
        qs = urlencode(data)
        headers = self.get_headers(url=url, data=data)
        return requests.get(url=url, params=qs, headers=headers)


class SandboxClient(BaseClient):
    sandbox = 'https://sandbox-api-pay.line.me/'


class Client(BaseClient):
    host = 'https://api-pay.line.me/'
