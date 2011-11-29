import json
import datetime
import feedparser

from gevent.pywsgi import WSGIServer

from gservice.core import Service
from gservice.config import Setting

from . import web
from .util import random_color
from .util import tinyid

class Bin(object):
    def __init__(self, private=False):
        self.private = private
        self.color = random_color()
        self.name = tinyid(8)
        self.requests = []
    
    def json(self):
        return json.dumps(dict(
            private=self.private, 
            color=self.color, 
            name=self.name,
            requests=self.requests))
    
    def add(self, request):
        self.requests.insert(0, Request(self, request))

class Request(object):
    def __init__(self, bin, input):
        self.bin = bin
        self.id = tinyid(6)
        self.created = datetime.datetime.now()
        self.remote_addr = input.remote_addr
        self.method = input.method
        self.headers = dict(input.headers)
        self.query_string = input.query_string
        self.form_data = []
        for k in input.values:
            self.form_data.append([k, input.values[k]])
        self.body = input.data
        self.path = input.path
        self.content_length = input.content_length
        self.content_type = input.content_type
    
    def __iter__(self):
        out = []
        if self.form_data:
            if hasattr(self.form_data, 'items'):
                items = self.form_data.items()
            else:
                items = self.form_data
            for k,v in items:
                try:
                    outval = json.dumps(json.loads(v), sort_keys=True, indent=2)
                except (ValueError, TypeError):
                    outval = v
                out.append((k, outval))
        else:
            try:
                out = (('body', json.dumps(json.loads(self.body), sort_keys=True, indent=2)),)
            except (ValueError, TypeError):
                out = (('body', self.body),)

        # Sort by field/file then by field name
        files = list()
        fields = list()
        for (k,v) in out:
            if type(v) is dict:
                files.append((k,v))
            else:
                fields.append((k,v))
        return iter(sorted(fields) + sorted(files))

class RequestBin(Service):
    bind_address = Setting('bind_address', default=('0.0.0.0', 5000))
    docs_url = Setting('docs_url', default='https://github.com/progrium/requestbin/wiki.atom')
    
    def __init__(self):
        self.server = WSGIServer(self.bind_address, web.app)
        self.add_service(self.server)
        
        web.app.config['service'] = self
        
        self.bins = {}
        self.private_bins = {}
        self.docs = None
    
    def do_start(self):
        self.docs = feedparser.parse(self.docs_url)
    
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