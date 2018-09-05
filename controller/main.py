import json

from agents.builder import build_agent_by_name
from constants import app
from flask import request
from flask import make_response
from routes import APP_ROUTES
from views.main import IframeView


# routes
webhook_route = APP_ROUTES.get('webhooks')
index_route = APP_ROUTES.get('index')


class Controller(object):

    @app.route(webhook_route.get('route'), methods=webhook_route.get('methods'))
    def webhook():
        post = request.get_json(silent=True, force=True)
        agent = build_agent_by_name('Event')
        return_value = agent.process(post)
        return_value = json.dumps(return_value, indent=4)
        # Convert the return value from a view function to an instance of response_class.
        response = make_response(return_value)
        response.headers['Content-Type'] = 'application/json'
        return response

    @app.route(index_route.get('route'))
    def index():
        iframe = IframeView()
        return iframe.render()
