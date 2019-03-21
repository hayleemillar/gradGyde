from flask import Flask

app = Flask("gradGyde")
app.config.from_pyfile('config.py')
secret_key = app.config['SECRET_KEY']

from . import main