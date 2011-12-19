import feedparser
import time

import gevent
from gevent.pywsgi import WSGIServer

from gservice.core import Service
from gservice.config import Setting

from . import web
from .models import Bin

class RequestBin(Service):
    bind_address = Setting('bind_address', default=('0.0.0.0', 5000))
    docs_url = Setting('docs_url', default='https://github.com/progrium/requestbin/wiki.atom')
    bin_ttl = Setting('bin_ttl', default=48*3600)
    cleanup_interval = Setting('cleanup_interval', default=3600)

    def __init__(self):
        self.server = WSGIServer(self.bind_address, web.app)
        self.add_service(self.server)

        web.app.config['service'] = self

        self.bins = {}
        self.docs = None

    def do_start(self):
        self.docs = feedparser.parse(self.docs_url)
        self.spawn(self._cleanup_loop)

    def _cleanup_loop(self):
        while True:
            gevent.sleep(self.cleanup_interval)
            self.expire_bins()

    def expire_bins(self):
        expiry = time.time() - self.bin_ttl
        for name, bin in self.bins.items():
            if bin.created < expiry:
                self.bins.pop(name)

    def create_bin(self, private=False):
        bin = Bin(private)
        self.bins[bin.name] = bin
        return self.bins[bin.name]

    def lookup_bin(self, name):
        return self.bins[name]

    def lookup_doc(self, name):
        matches = [{'title': e.title, 'content': e.content[0].value}
                    for e in self.docs.entries if e.links[0].href.split('/')[-1] == name]
        if matches:
            return matches[0]
