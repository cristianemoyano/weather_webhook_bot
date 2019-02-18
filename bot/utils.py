import datetime
from dateutil import tz

from bot.chatbot_plugin.app.controller.utils import (
    get_intent_display_name,
    get_agent_name,
    get_lang_code,
)


def get_required_params(post, url):
    intent_display_name = get_intent_display_name(post)
    agent_name = get_agent_name(post)
    agent_name_defined = intent_display_name or agent_name
    lang_code = get_lang_code(post)
    return {
        'agent_name': agent_name_defined,
        'url': url,
        'lang_code': lang_code,
        'params': post,
    }


def get_datetime_in_utc():
    """Returns date in UTC w/o tzinfo"""
    date = datetime.datetime.utcnow()
    timestamp = date.astimezone(tz.gettz('UTC')).replace(tzinfo=None) if date.tzinfo else date
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")
