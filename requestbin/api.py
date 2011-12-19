import json
from flask import session, make_response, request, render_template

from .web import app

@app.endpoint('api.bins')
def bins():
    private = request.form.get('private') == 'true'
    bin = app.config['service'].create_bin(private)
    if bin.private:
        session[bin.name] = bin.secret_key
    jsonp = request.args.get('jsonp')
    if jsonp:
        resp = make_response('%s(%s)' % (jsonp, bin.json()), 200)
        resp.headers['Content-Type'] = 'text/javascript'
    else:
        resp = make_response(bin.json(), 200)
        resp.headers['Content-Type'] = 'application/json'
        resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
