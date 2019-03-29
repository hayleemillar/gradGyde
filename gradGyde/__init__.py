# pylint: disable=invalid-name
import os
from flask import Flask
from . import main


app = Flask("gradGyde")
app.secret_key = os.getenv('SECRET_KEY')
