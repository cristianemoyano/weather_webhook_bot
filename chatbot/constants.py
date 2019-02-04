import os
from flask import Flask
from dotenv import load_dotenv
from os.path import join, dirname

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)

# Testing
DEBUG = bool(int(os.environ.get('DEBUG')))
# Eventbrite Integration
EB_ACCESS_TOKEN = os.environ.get('EB_ACCESS_TOKEN')
EB_ORGANIZATION_ID = os.environ.get('EB_ORGANIZATION_ID')
EB_IS_BY_ORGANIZATION = bool(int(os.environ.get('EB_IS_BY_ORGANIZATION')))
# App port
PORT = int(os.environ.get('PORT', 5000))
# Facebook integration
FB_MESSENGER_ACCESS_TOKEN = os.environ.get('FB_MESSENGER_ACCESS_TOKEN')
FB_INBOX_APP_ID = os.environ.get('FB_INBOX_APP_ID')
# OpenWeatherMap integration
OPENWEATHERMAP_KEY = os.environ.get('OPENWEATHERMAP_KEY')
# Log file handler is active
IS_LOG_FILE_HANDLER_ACTIVE = bool(int(os.environ.get('IS_LOG_FILE_HANDLER_ACTIVE')))
# Celery
app.config['CELERY_BROKER_URL'] = os.environ.get('CLOUDAMQP_URL')
app.config['RESULT_BACKEND'] = os.environ.get('CLOUDAMQP_URL')

ROOT_PATH = os.getcwd()
