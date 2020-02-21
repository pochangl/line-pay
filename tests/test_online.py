import line_sdk
from .utils import create_orderId

credentials = {}


def create_request_data():
    'generate simple request data'

    return dict(
        orderId=create_orderId(),
        amount=100,
        currency='TWD',
        packages=[
            dict(
                id=1,
                amount=100,
                name='package1',
                products=[
                    dict(
                        id=2,
                        name='product2',
                        price=50,
                        quantity=2
                    )
                ]
            )
        ],
        redirectUrls=dict(
            confirmUrl='https://example.com/confirm',
            cancelUrl='https://example.com/cancel'
        )
    )


def test_request(self):
    client = line_sdk.Client(**credentials)
    data = create_request_data()
    rtn = client.pay.online.request(**data)

    assert rtn['returnCode'] == '0000', rtn

    transactionId = rtn['info']['transactionId']
    status = client.pay.online.status(transactionId=transactionId)

    assert status['returnCode'] == '0000'
