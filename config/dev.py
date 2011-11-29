bind_address = ('0.0.0.0', 5000)

def service():
    from requestbin.service import RequestBin
    return RequestBin()