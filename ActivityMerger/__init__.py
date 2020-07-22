import os
from flask import Flask
from flask_assets import Environment as FlaskAssets, Bundle


app = Flask(__name__)

app.config.from_object('config.Config')
app.secret_key = app.config['SECRET_KEY']

assets = FlaskAssets(app)
assets.register('js_base', Bundle(
    os.path.join('js', 'jquery-1.12.4.js'),
    os.path.join('js', 'bootstrap-3.3.7.js'),
    filters='jsmin',
    output=os.path.join('gen', 'js.%(version)s.min.js'))
)
assets.register('js_activity', Bundle(
    os.path.join('js', 'activity.js'),
    filters='jsmin',
    output=os.path.join('gen', 'activity.%(version)s.min.js'))
)
assets.register('css_base', Bundle(
    os.path.join('css', 'bootstrap.css'),
    os.path.join('css', 'font-awesome.css'),
    os.path.join('css', 'app.css'),
    filters='cssmin',
    output=os.path.join('gen', 'css.%(version)s.min.css'))
)

from ActivityMerger import routes, commands
