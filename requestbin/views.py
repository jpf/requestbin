import urllib

from flask import session, redirect, url_for, escape, request, render_template

from .web import app
from .util import solid16x16gif_datauri

@app.endpoint('views.home')
def home():
    return render_template('home.html')

@app.endpoint('views.bin')
def bin(name):
    try:
        bin = app.config['service'].lookup_bin(name)
        if request.query_string == 'inspect':
            return render_template('bin.html', 
                favicon_uri=solid16x16gif_datauri(*bin.color),
                bin=bin,
                host=request.host)
        else:
            bin.add(request)
            return "OK\n"
    except KeyError:
        return "Not found", 404

@app.endpoint('views.docs')
def docs(name):
    doc = app.config['service'].lookup_doc(name)
    if doc:
        return render_template('doc.html', content=doc['content'], title=doc['title'])
    else:
        return "Not found", 404