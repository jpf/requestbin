from flask import Flask, redirect

app = Flask(__name__)
app.debug = True
app.secret_key = '((Z O*T^@YX R~XHH!jesrgwerg]LWerg@#R#$TT'

app.add_url_rule('/', 'views.home')
app.add_url_rule('/<name>', 'views.bin', methods=['GET', 'POST', 'DELETE', 'PUT', 'OPTIONS', 'HEAD'])

app.add_url_rule('/docs/<name>', 'views.docs')
app.add_url_rule('/api/v1/bins', 'api.bins', methods=['POST'])
app.add_url_rule('/api/v1/stats', 'api.stats')

app.add_url_rule('/favicon.ico', view_func=lambda: redirect('/static/favicon.ico'))
app.add_url_rule('/robots.txt', view_func=lambda: redirect('/static/robots.txt'))

from . import views
from . import api
