import os

bind_address = ('0.0.0.0', int(os.environ.get("PORT", 5000)))

def service():
    from requestbin.service import RequestBin
    return RequestBin()