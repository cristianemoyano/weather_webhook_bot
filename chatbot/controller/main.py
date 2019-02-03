from flask import jsonify

from .flask_celery import process_webhook
from .exceptions import InvalidUsage
from .utils import (
    get_methods,
    get_route,
)
from chatbot.agents.builder import (
    build_agent_by_intent_diplayname,
)
from chatbot.constants import app
from flask import (
    request,
    make_response,
)
from chatbot.views.main import (
    IframeView,
    WebView,
    SandboxView,
)


class Controller(object):

    @app.errorhandler(InvalidUsage)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.route(get_route('webhooks'), methods=get_methods('webhooks'))
    def webhook():
        post = request.get_json(silent=True, force=True)
        print(post)
        return process_webhook(post)

    @app.route(get_route('index'))
    def index():
        iframe = IframeView()
        return iframe.render()

    @app.route(get_route('webview'))
    def webview():
        webview = WebView()
        response = make_response(webview.render())
        response.headers['Content-Type'] = 'text/html'
        return response

    @app.route(get_route('sandbox'), methods=get_methods('sandbox'))
    def sandbox():
        agent = build_agent_by_intent_diplayname('SandBox')
        if request.method == 'POST':
            form = request.form
            post = form.to_dict()
            agent.process_request(post)
        sandbox = SandboxView()
        return sandbox.render()
