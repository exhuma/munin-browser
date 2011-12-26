import logging

from flask import Flask, g, abort, render_template

from muninbrowser.model import Munin

LOG = logging.getLogger(__name__)
app = Flask(__name__)
app.config.from_object('muninbrowser.default_settings')
app.config.from_envvar('MUNINBROWSER_CONFIG', silent=True)

@app.before_request
def before_request():
    g.model = Munin(app.config['MUNIN_CONF'])
    g.model.cache = app.config['MUNIN_CACHE']

@app.route("/", methods=['GET'])
def index():
    return render_template('index.html',
            tree = g.model.tree)

