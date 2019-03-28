# pylint: disable=invalid-name
from flask import Flask
import os
from . import main

app = Flask("gradGyde")
app.config.from_pyfile('config.py')
secret_key = app.config['SECRET_KEY'] #os.getenv('SECRET_KEY')
