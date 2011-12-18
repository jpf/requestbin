import os

bind_address = ('0.0.0.0', int(os.environ.get("PORT", 5000)))
ignore_headers = """
X-Varnish
X-Forwarded-For
X-Heroku-Dynos-In-Use
X-Request-Start
X-Heroku-Queue-Wait-Time
X-Heroku-Queue-Depth
""".split("\n")[1:-1]

def service():
    from requestbin.service import RequestBin
    return RequestBin()
