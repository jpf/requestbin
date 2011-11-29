import json
from flask import make_response, request, render_template

from .web import app

@app.endpoint('api.bins')
def bins():
    bin = app.config['service'].create_bin()
    resp = make_response(bin.json(), 200)
    resp.headers['Content-Type'] = 'application/json'
    return resp