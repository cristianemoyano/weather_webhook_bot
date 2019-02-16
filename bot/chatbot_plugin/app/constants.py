import os

# Testing
DEBUG = bool(int(os.getenv('DEBUG')))
# Eventbrite Integration
EB_ACCESS_TOKEN = os.getenv('EB_ACCESS_TOKEN')
EB_ORGANIZATION_ID = os.getenv('EB_ORGANIZATION_ID')
EB_IS_BY_ORGANIZATION = bool(int(os.getenv('EB_IS_BY_ORGANIZATION')))
# App port
PORT = int(os.getenv('PORT', 5000))
# Facebook integration
FB_MESSENGER_ACCESS_TOKEN = os.getenv('FB_MESSENGER_ACCESS_TOKEN')
FB_INBOX_APP_ID = os.getenv('FB_INBOX_APP_ID')
# OpenWeatherMap integration
OPENWEATHERMAP_KEY = os.getenv('OPENWEATHERMAP_KEY')
# Log file handler is active
IS_LOG_FILE_HANDLER_ACTIVE = bool(int(os.getenv('IS_LOG_FILE_HANDLER_ACTIVE')))

ROOT_PATH = os.getcwd()
