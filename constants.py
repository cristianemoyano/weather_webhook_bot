import os

from flask import Flask

app = Flask(__name__)

DEBUG = bool(int(os.environ['DEBUG']))
EB_ACCESS_TOKEN = os.environ['EB_ACCESS_TOKEN']
PORT = int(os.getenv('PORT', 5000))
