import json

from chatbot.constants import app
from .flask_celery import make_celery

from chatbot.agents.builder import (
    build_agent_by_intent_diplayname,
)

celery = make_celery(app)


@celery.task(name='chatbot.tasks.process_webhook')
def process_webhook(agent_name, url, lang_code, params, *args, **kwargs):
    if agent_name:
        agent = build_agent_by_intent_diplayname(agent_name)
        agent.request_url = url
        # param: languageCode
        agent.lang_code = lang_code
        try:
            return_value = agent.process_request(params)
            return_value = json.dumps(return_value, indent=4)
            print(return_value)
        except Exception as e:
            print('Internal error: {}'.format(e))
    else:
        print('Invalid usage: Agent not defined')
