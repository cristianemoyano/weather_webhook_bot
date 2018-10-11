import requests

from chatbot.integrations.base import Integration
from chatbot.constants import FB_MESSENGER_ACCESS_TOKEN
from chatbot.integrations.exceptions import UndefinedElementType


FB_SENDER_ACTIONS = {
    'seen': 'mark_seen',
    'typing_on': 'typing_on',
    'typing_off': 'typing_off',
}


class FacebookSimpleElement(object):
    def get_element(
        self,
        title,
        sub,
        image_url,
        btn_title,
        btn_url,
        webview
    ):
        element = {
            'title': title,
            'subtitle': sub,
            'image_url': image_url,
            'buttons': [
                {
                    "title": "View",
                    "type": "web_url",
                    "url": btn_url,
                    "messenger_extensions": "false",
                    "webview_height_ratio": "tall",
                },
                {
                    "type": "web_url",
                    "url": webview,
                    "title": 'Tickets',
                    "messenger_extensions": "true",
                    "webview_height_ratio": "full"
                },
                {
                    "type": "postback",
                    "title": "more events",
                    "payload": "DEVELOPER_DEFINED_PAYLOAD"
                }
            ],
            "default_action": {
                "type": "web_url",
                "url": btn_url,
                "messenger_extensions": "false",
                "webview_height_ratio": "tall",
            },
        }

        return element


class FacebookComplexElement(object):
    def get_element(
        self,
        title,
        sub,
        image_url,
        btn_title,
        btn_url,
        webview
    ):
        element = {
            'title': title,
            'subtitle': sub,
            'image_url': image_url,
            "default_action": {
                "type": "web_url",
                "url": btn_url,
                "messenger_extensions": False,
                "webview_height_ratio": "tall",
                "fallback_url": btn_url
            },
            'buttons': [
                {
                    "type": "web_url",
                    "url": btn_url,
                    "title": "View"
                },
                {
                    "type": "postback",
                    "title": "Thanks",
                    "payload": "DEVELOPER_DEFINED_PAYLOAD"
                }
            ],
        }
        return element


class FacebookIntegration(Integration):
    """docstring for FacebookIntegration"""

    ELEMENTS_TYPE = {
        'simple': FacebookSimpleElement,
        'complex': FacebookComplexElement,
    }

    QUICK_REPLIES = {
        'location': {
            'text': 'Please share your location:',
            'type': 'location',
        },
        'phone': {
            'text': 'Please share your phone number:',
            'type': 'user_phone_number',
        },
        'email': {
            'text': 'Please share your email:',
            'type': 'user_email',
        },
        'list_options': {
            'text': 'Check more events?',
            'elements_example': [
                {
                    "content_type": "text",
                    "title": "Yes, more !",
                    "payload": "more events"
                },
                {
                    "content_type": "text",
                    "title": "No, thanks!",
                    "payload": "thank you"
                },

            ],
        }
    }

    def __init__(self, call_url='https://graph.facebook.com/v3.1/me/messages'):
        super(FacebookIntegration, self).__init__()
        self.fb_token = FB_MESSENGER_ACCESS_TOKEN
        self.call_url = call_url

    def display_sender_action(self, sender_id, sender_action):
        json_data = {
            "recipient": {"id": sender_id},
            "sender_action": sender_action
        }
        params = {
            "access_token": self.fb_token
        }
        r = requests.post(
            self.call_url,
            json=json_data,
            params=params
        )
        print(r, r.status_code, r.text)
        print(sender_id)
        print(json_data)

    def respond(self, sender_id, typeMessage, elements=None, is_quick_reply=False):
        json_data = {
            "recipient": {"id": sender_id},
            "messaging_type": "response",
            "message": self.get_message(
                elements=elements,
                typeMessage=typeMessage,
                is_quick_reply=is_quick_reply
            )
        }

        params = {
            "access_token": self.fb_token
        }
        r = requests.post(
            self.call_url,
            json=json_data,
            params=params
        )
        print(r, r.status_code, r.text)
        print(sender_id)
        print(json_data)

    def get_message(self, typeMessage, elements=None, is_quick_reply=False):
        msg = {}
        if elements and not is_quick_reply:
            if typeMessage == 'template':
                msg.update({
                    "attachment": {
                        "type": "template",
                        "payload": {
                            "template_type": "generic",
                            "elements": elements
                        }
                    }
                })
        if is_quick_reply:
            msg.update(self.get_quick_reply(typeMessage, elements))
        return msg

    def get_quick_reply(self, typeMessage, elements=None):
        reply = self.QUICK_REPLIES.get(typeMessage)
        msg = {
            "text": reply.get('text'),
            "quick_replies": [
                {
                    "content_type": reply.get('type')
                }
            ]
        }
        if typeMessage == 'list_options':
            msg.update({
                "text": reply.get('text'),
                "quick_replies": reply.get('elements_example')
            })
        return msg

    def get_element(self, element_type, title, sub, image_url, btn_title, btn_url, webview):
        element = self.ELEMENTS_TYPE.get(element_type, None)
        if element:
            return element().get_element(title, sub, image_url, btn_title, btn_url, webview)
        else:
            raise UndefinedElementType(element_type)
