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
        btn_url
    ):
        element = {
            "title": title,
            "subtitle": sub,
            "image_url": image_url,
            "buttons": [{
                "title": btn_title,
                "type": "web_url",
                "url": btn_url,
                "messenger_extensions": "false",
                "webview_height_ratio": "full"
            }],
            "default_action": {
                "type": "web_url",
                "url": btn_url,
                "messenger_extensions": "false",
                "webview_height_ratio": "full"
            }
        }

        return element


class FacebookComplexElement(object):
    def get_element(
        self,
        title,
        sub,
        image_url,
        btn_title,
        btn_url
    ):
        element = {
            'title': title,
            'subtitle': sub,
            'item_url': btn_url,
            'image_url': image_url,
            'buttons':
                [
                    {
                        "type": "payment",
                        "title": "buy",
                        "payload": "ticket_type_vip",
                        "payment_summary": {
                            "currency": "USD",
                            "payment_type": "FIXED_AMOUNT",
                            "is_test_payment": "true",
                            "merchant_name": "Eventbrite",
                            "requested_user_info": [
                                "contact_email"
                            ],
                            "price_list":[
                                {
                                    "label": "Subtotal",
                                    "amount": "1.00"
                                }
                            ]
                        }
                    },
                    {
                        "title": "$100 Get tickets",
                        'type': 'web_url',
                        "url": "https://mulberry-surf.glitch.me/webview",
                        "webview_height_ratio": "tall",
                        "messenger_extensions": "true",
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

    def get_element(self, element_type, title, sub, image_url, btn_title, btn_url):
        element = self.ELEMENTS_TYPE.get(element_type, None)
        if element:
            return element().get_element(title, sub, image_url, btn_title, btn_url)
        else:
            raise UndefinedElementType(element_type)
