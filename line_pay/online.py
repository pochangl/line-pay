class API:
    endpoint = ''

    def __ini__(self, client):
        self.client = client

    def get_endpoint(self, **data):
        return self.endpoint.format(data)

    def post(self, data, kwargs={}):
        return self.client.post(url=self.get_endpoint(**kwargs), data=data)

    def get(self, data={}, kwargs={}):
        return self.client.get(url=self.get_endpoint(**kwargs), data=data)


class RequestAPI(API):
    'refer to https://pay.line.me/documents/online_v3_en.html#request-api'

    endpoint = '/v3/payments/request'

    def send(
            self, orderId: str, amount: int, currency: str,
            packages: list, redirectUrls: dict, options: dict):

        data = dict(
            orderId=orderId,
            amount=amount,
            currency=currency,
            packages=packages,
            redirectUrls=redirectUrls,
        )
        return self.post(data=data)


class ConfirmAPI(API):
    'refer to https://pay.line.me/documents/online_v3_en.html#confirm-api'

    endpoint = '/v3/payments/{transactionId}/confirm'

    def send(self, transactionId, currency, amount):
        data = dict(
            currency=currency,
            amount=amount,
        )
        kwargs = dict(
            transactionId=transactionId,
        )
        return self.post(data=data, kwargs=kwargs)


class StatusAPI(API):
    endpoint = '/v3/payments/requests/{transactionId}/check'

    def send(self, transactionId):
        kwargs = dict(
            transactionId=transactionId
        )
        return self.get(kwargs=kwargs)
