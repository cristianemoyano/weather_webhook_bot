import json
from flask import jsonify

from chatbot.tasks import process_webhook
from .exceptions import InvalidUsage
from .utils import (
    get_methods,
    get_route,
    get_intent_display_name,
    get_agent_name,
    get_lang_code,
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
        post_data = request.get_json(silent=True, force=True)
        intent_display_name = get_intent_display_name(post_data)
        agent_name = get_agent_name(post_data)
        agent_name_defined = intent_display_name or agent_name
        lang_code = get_lang_code(post_data)
        data = {
            'agent_name': agent_name_defined,
            'url': request.url,
            'lang_code': lang_code,
            'params': post_data,
        }
        print(data)
        if request.method == 'POST':
            process_webhook.delay(**data)
            return 'async request sent'
        elif request.method == 'GET':
            get_data = request.args
            agent = build_agent_by_intent_diplayname(get_data.get('agent', None))
            agent.request_url = request.url
            agent.lang_code = get_data.get('lang_code', None)
            try:
                return_value = agent.process_request(get_data)
                return_value = json.dumps(return_value, indent=4)
                return return_value
            except Exception as e:
                raise InvalidUsage('Internal error: {}'.format(e), status_code=500)
        else:
            raise InvalidUsage('Invalid usage: Agent not defined', status_code=410)

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
