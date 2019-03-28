# pylint: disable=invalid-name
import os
from flask import Flask


app = Flask("gradGyde")
app.secret_key = os.getenv('SECRET_KEY')

from . import main
