import requests

from integrations.base import Integration
from constants import FB_MESSENGER_ACCESS_TOKEN


class FacebookIntegration(Integration):
    """docstring for FacebookIntegration"""
    def __init__(self, call_url='https://graph.facebook.com/v2.6/me/messages'):
        super(FacebookIntegration, self).__init__()
        self.fb_token = FB_MESSENGER_ACCESS_TOKEN
        self.call_url = call_url

    def respond(self, sender_id):
        msg = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                        {
                            "title": "Hello 1",
                            "subtitle": "Subtitle 1",
                            "image_url": "https://cdn-images-1.medium.com/1*Vkf6A8Mb0wBoL3Fw1u0paA.jpeg",
                            "buttons": [{
                                "title": "View",
                                "type": "web_url",
                                "url": "https://www.medium.com/",
                                "messenger_extensions": "false",
                                "webview_height_ratio": "full"
                            }],
                            "default_action": {
                                "type": "web_url",
                                "url": "https://www.medium.com/",
                                "messenger_extensions": "false",
                                "webview_height_ratio": "full"
                            }
                        },
                        {
                            "title": "Hello 2",
                            "subtitle": "Subtitle 2",
                            "image_url": "https://cdn-images-1.medium.com/1*Vkf6A8Mb0wBoL3Fw1u0paA.jpeg",
                            "buttons": [{
                                "title": "View",
                                "type": "web_url",
                                "url": "https://www.medium.com/",
                                "messenger_extensions": "false",
                                "webview_height_ratio": "full"
                            }],
                            "default_action": {
                                "type": "web_url",
                                "url": "https://www.medium.com/",
                                "messenger_extensions": "false",
                                "webview_height_ratio": "full"
                            }
                        }
                    ]
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
