import datetime
from dateutil import tz

from bot.chatbot_plugin.app.controller.utils import (
    get_intent_display_name,
    get_agent_name,
    get_lang_code,
)
from .chatbot_plugin.app.integrations.facebook import FacebookIntegration


def get_page_data(token):
    """
    {
        "data":
            [
                {
                    "access_token":"",
                    "category":"Event",
                    "category_list":[{"id":"192119584190796","name":"Event"}],
                    "name":"Search Events","id":"256171418366507",
                    "tasks":["ANALYZE","ADVERTISE","MODERATE","CREATE_CONTENT","MANAGE"]
                },
                {
                    "access_token":"",
                    "category":"Entertainment Website",
                    "category_list":[{"id":"2705","name":"Entertainment Website"}],
                    "name":"Chatbot +Con",
                    "id":"297439270861658",
                    "tasks":["ANALYZE","ADVERTISE","MODERATE","CREATE_CONTENT","MANAGE"]
                },
                {
                    "access_token":"",
                    "category":"Comedian",
                    "category_list":[{"id":"1610","name":"Comedian"}],
                    "name":"Chatbot del 8",
                    "id":"1828290267463099",
                    "tasks":["ANALYZE","ADVERTISE","MODERATE","CREATE_CONTENT"]
                }
            ],
            "paging":
                {
                    "cursors":
                        {
                            "before":"","after":""
                        }
                }
    }
    """
    fb_client = FacebookIntegration()
    return fb_client.get_page_data(token)


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
