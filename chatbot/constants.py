import os
from flask import Flask
from dotenv import load_dotenv
from os.path import join, dirname

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)


DEBUG = bool(int(os.environ.get('DEBUG')))
EB_ACCESS_TOKEN = os.environ.get('EB_ACCESS_TOKEN')
PORT = int(os.environ.get('PORT', 5000))
FB_MESSENGER_ACCESS_TOKEN = os.environ.get('FB_MESSENGER_ACCESS_TOKEN')
OPENWEATHERMAP_KEY = os.environ.get('OPENWEATHERMAP_KEY')

ROOT_PATH = os.getcwd()
