import urllib

from flask import session, redirect, url_for, escape, request, render_template

from .web import app

def update_recent_bins(name):
    if 'recent' not in session:
        session['recent'] = []
    if name in session['recent']:
        session['recent'].remove(name)
    session['recent'].insert(0, name)
    if len(session['recent']) > 10:
        session['recent'] = session['recent'][:10]
    session.modified = True

def expand_recent_bins():
    if 'recent' not in session:
        session['recent'] = []
    recent = []
    for name in session['recent']:
        try:
            recent.append(app.config['service'].lookup_bin(name))
        except KeyError:
            session['recent'].remove(name)
            session.modified = True
    return recent

@app.endpoint('views.home')
def home():
    return render_template('home.html', recent=expand_recent_bins())

@app.endpoint('views.bin')
def bin(name):
    try:
        bin = app.config['service'].lookup_bin(name)
        if request.query_string == 'inspect':
            if bin.private and session.get(bin.name) != bin.secret_key:
                return "Private bin\n", 403
            update_recent_bins(name)
            return render_template('bin.html',
                bin=bin,
                host=request.host)
        else:
            bin.add(request)
            return "ok\n"
    except KeyError:
        return "Not found\n", 404

@app.endpoint('views.docs')
def docs(name):
    doc = app.config['service'].lookup_doc(name)
    if doc:
        return render_template('doc.html',
                content=doc['content'],
                title=doc['title'],
                recent=expand_recent_bins())
    else:
        return "Not found", 404
