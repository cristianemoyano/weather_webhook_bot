import json

from chatbot.agents.builder import build_agent_by_intent_diplayname
from chatbot.constants import app
from flask import request
from flask import make_response
from chatbot.routes import APP_ROUTES
from chatbot.views.main import IframeView, WebView


# routes
webhook_route = APP_ROUTES.get('webhooks')
index_route = APP_ROUTES.get('index')
webview_route = APP_ROUTES.get('webview')


def get_intent_display_name(post):
    intent_display_name = None
    try:
        intent_display_name = post.get('queryResult').get('intent').get('displayName')
    except AttributeError:
        intent_display_name = None

    try:
        intent_display_name = intent_display_name or post.get('result').get('action')
    except AttributeError:
        intent_display_name = None

    return intent_display_name


class Controller(object):

    @app.route(webhook_route.get('route'), methods=webhook_route.get('methods'))
    def webhook():
        post = request.get_json(silent=True, force=True)
        print(post)
        intent_display_name = get_intent_display_name(post)
        agent = build_agent_by_intent_diplayname(intent_display_name)
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

    @app.route(webview_route.get('route'))
    def webview():
        webview = WebView()
        response = make_response(webview.render())
        response.headers['Content-Type'] = 'text/html'
        response.headers['X-Frame-Options'] = 'ALLOW-FROM: https://www.messenger.com/'
        response.headers['X-Frame-Options'] = 'ALLOW-FROM: https://www.facebook.com/'
        return response
