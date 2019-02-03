import json
from .exceptions import InvalidUsage
from flask import (
    request,
    make_response,
)

from .utils import (
    get_intent_display_name,
    get_agent_name,
    get_lang_code,
)
from chatbot.agents.builder import (
    build_agent_by_intent_diplayname,
)


def process_webhook(post):
    intent_display_name = get_intent_display_name(post)
    agent_name = get_agent_name(post)
    agent_name_defined = intent_display_name or agent_name
    if agent_name_defined:
        agent = build_agent_by_intent_diplayname(agent_name_defined)
        agent.request_url = request.url
        # param: languageCode
        agent.lang_code = get_lang_code(post)
        try:
            return_value = agent.process_request(post)
            return_value = json.dumps(return_value, indent=4)
            # Convert the return value from a view function to an instance of response_class.
            response = make_response(return_value)
            response.headers['Content-Type'] = 'application/json'
            return response
        except Exception as e:
            raise InvalidUsage('Internal error: {}'.format(e), status_code=500)
    raise InvalidUsage('Invalid usage: Agent not defined', status_code=410)
