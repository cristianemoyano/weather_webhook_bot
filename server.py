import os

from routes import APP_ROUTES
from constants import (
    DEBUG,
    PORT,
    app
)
from controller.main import Controller

# routes
webhook_route = APP_ROUTES.get('webhooks')
index_route = APP_ROUTES.get('index')

if __name__ == '__main__':
    Controller()
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % PORT)
    app.run(debug=DEBUG, port=PORT, host='0.0.0.0')
