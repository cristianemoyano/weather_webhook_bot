import json

from chatbot.controller.utils import (
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

    @app.route(get_route('webhooks'), methods=get_methods('webhooks'))
    def webhook():
        post = request.get_json(silent=True, force=True)
        print(post)
        intent_display_name = get_intent_display_name(post)
        agent_name = get_agent_name(post)
        if intent_display_name:
            agent = build_agent_by_intent_diplayname(intent_display_name)
            agent.request_url = request.url
            # param: languageCode
            agent.lang_code = get_lang_code(post)
            return_value = agent.process_request(post)
            return_value = json.dumps(return_value, indent=4)
            # Convert the return value from a view function to an instance of response_class.
            response = make_response(return_value)
            response.headers['Content-Type'] = 'application/json'
            return response
        elif agent_name:
            # param: agent
            agent = build_agent_by_intent_diplayname(agent_name)
            agent.request_url = request.url
            # param: lang_code
            agent.lang_code = get_lang_code(post)
            return_value = agent.process_request(post)
            return_value = json.dumps(return_value, indent=4)
            # Convert the return value from a view function to an instance of response_class.
            response = make_response(return_value)
            response.headers['Content-Type'] = 'application/json'
            return response

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
