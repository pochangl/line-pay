import time


def create_orderId():
    'generate order Id'

    ts = time.time()
    return str(int(ts * 1000))

CREDENTIALS = {}
