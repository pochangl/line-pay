import time
from functools import reduce
from unittest.mock import patch


def create_orderId():
    'generate order Id'

    ts = time.time()
    return str(int(ts * 1000))


class Wrapper:
    def __init__(self, data):
        self.data = data

    def json(self):
        return self.data


def request_patcher(**kwargs):
    return Wrapper(kwargs)


def patch_request(func):
    patches = [
        patch('requests.post', new=request_patcher),
        patch('requests.get', new=request_patcher),
    ]
    return reduce(lambda f, patch: patch(f), patches, func)
