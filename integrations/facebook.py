import requests

from integrations.base import Integration
from constants import FB_MESSENGER_ACCESS_TOKEN
from integrations.exceptions import UndefinedElementType


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
                    "title": "Dialog",
                    "type": "web_url",
                    "url": webview,
                    "messenger_extensions": "false",
                    "webview_height_ratio": "full",
                },
                {
                    "type": "postback",
                    "title": "Thanks",
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

    def __init__(self, call_url='https://graph.facebook.com/v2.6/me/messages'):
        super(FacebookIntegration, self).__init__()
        self.fb_token = FB_MESSENGER_ACCESS_TOKEN
        self.call_url = call_url

    def respond(self, sender_id, elements):
        msg = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": elements
                }
            }
        }
        json_data = {
            "recipient": {"id": sender_id},
            "message": msg
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

    def get_element(self, element_type, title, sub, image_url, btn_title, btn_url, webview):
        element = self.ELEMENTS_TYPE.get(element_type, None)
        if element:
            return element().get_element(title, sub, image_url, btn_title, btn_url, webview)
        else:
            raise UndefinedElementType(element_type)
