import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

DEBUG = bool(int(os.getenv('DEBUG')))
EB_ACCESS_TOKEN = os.getenv('EB_ACCESS_TOKEN')
PORT = int(os.getenv('PORT', 5000))
FB_MESSENGER_ACCESS_TOKEN = os.getenv('FB_MESSENGER_ACCESS_TOKEN')
OPENWEATHERMAP_KEY = os.getenv('OPENWEATHERMAP_KEY')

ROOT_PATH = os.getcwd()
