import requests


class BaseClient:
    def __init__(self, Authorization, AuthorizationNonce, ChannelId, MerchantDeviceProfileId=None):
        self.ChannelId = ChannelId
        self.MerchantDeviceProfileId = MerchantDeviceProfileId
        self.Authorization = Authorization
        self.AuthorizationNonce = AuthorizationNonce

    def get_headers(self):
        '''
            authentication headers
            refer to https://pay.line.me/documents/online_v3_en.html#api-authentication
        '''
        data = {
            'Content-Type': 'application/json',
            'X-LINE-ChannelId': self.ChannelId,
            'X-LINE-Authorization-Nonce': self.AuthorizationNonce,
            'X-LINE-Authorization': self.Authorization
        }

        if self.MerchantDeviceProfileId is not None:
            data['X-LINE-MerchantDeviceProfileId'] = self.MerchantDeviceProfileId
        return data

    def post(self, url, data):
        headers = self.get_headers()
        return requests.post(url=url, data=data, headers=headers, json=True)

    def get(self, url, data):
        headers = self.get_headers()
        return requests.get(url=url, params=data, headers=headers)


class SandboxClient(BaseClient):
    sandbox = 'https://sandbox-api-pay.line.me/'


class Client(BaseClient):
    host = 'https://api-pay.line.me/'
