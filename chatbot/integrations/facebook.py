import requests

from chatbot.integrations.base import Integration
from chatbot.constants import (
    FB_MESSENGER_ACCESS_TOKEN,
    FB_INBOX_APP_ID,
)
from chatbot.integrations.exceptions import UndefinedElementType


FB_SENDER_ACTIONS = {
    'seen': 'mark_seen',
    'typing_on': 'typing_on',
    'typing_off': 'typing_off',
}


class FacebookSimpleElement(object):

    BTN_TYPE_WEB_URL = "web_url"
    BTN_TYPE_POSTBACK = "postback"
    WEBVIEW_HEIGHT_RATIO_SMALL = "compact"
    WEBVIEW_HEIGHT_RATIO_MEDIUM = "tall"
    WEBVIEW_HEIGHT_RATIO_LARGE = "full"
    MSG_EXTENSION_TRUE = "true"
    MSG_EXTENSION_FALSE = "false"

    def __init__(self):
        self.buttons = []

    def add_button(self, btn_title, btn_type, msg_extension, webview_height):
        self.buttons.append({
            "title": btn_title,
            "type": btn_type,
            "url": None,
            "messenger_extensions": msg_extension,
            "webview_height_ratio": webview_height,
        })

    def add_postback_button(self, btn_title, btn_payload):
        self.buttons.append({
            'type': self.BTN_TYPE_POSTBACK,
            'title': btn_title,
            'payload': btn_payload
        })

    def add_url_and_get_buttons(self, btn_url, buttons, webview=None):
        for btn in buttons:
            if not hasattr(btn, 'payload'):
                btn['url'] = btn_url
            if (
                btn.get('messenger_extensions') == self.MSG_EXTENSION_TRUE and
                btn.get('webview_height_ratio') == self.WEBVIEW_HEIGHT_RATIO_LARGE and
                webview
            ):
                btn['url'] = webview
        return buttons

    def get_element(
        self,
        title,
        subtitle,
        image_url,
        btn_title,
        btn_url,
        webview,
        msg_extension,
        webview_height_ratio,
        buttons
    ):
        element = {
            "title": title,
            "subtitle": subtitle,
            "image_url": image_url,
            "buttons": self.add_url_and_get_buttons(btn_url, buttons, webview),
            "default_action": {
                "type": self.BTN_TYPE_WEB_URL,
                "url": btn_url,
                "messenger_extensions": self.MSG_EXTENSION_FALSE,
                "webview_height_ratio": self.WEBVIEW_HEIGHT_RATIO_MEDIUM,
            },
        }
        return element


class FacebookIntegration(Integration):
    """docstring for FacebookIntegration"""

    def __init__(self, call_url='https://graph.facebook.com/v3.1/me/messages'):
        super(FacebookIntegration, self).__init__()
        self.fb_token = FB_MESSENGER_ACCESS_TOKEN
        self.app_id = FB_INBOX_APP_ID
        self.ELEMENTS_TYPE_SIMPLE = 'simple'
        self.ELEMENTS_TYPES = {
            self.ELEMENTS_TYPE_SIMPLE: FacebookSimpleElement,
        }
        # Doc: https://developers.facebook.com/docs/messenger-platform/send-messages/templates
        self.FB_MESSAGE_TYPE_TEMPLATE = 'template'
        self.FB_TEMPLATE_TYPE_GENERIC = 'generic'
        self.call_url = call_url

    def send_pass_thread(self, sender_id):
        uri = 'https://graph.facebook.com/v2.6/me/pass_thread_control'
        json_data = {
            "recipient": {
                "id": sender_id
            },
            "target_app_id": self.app_id
        }

        params = {
            "access_token": self.fb_token
        }
        r = requests.post(
            uri,
            json=json_data,
            params=params
        )
        print(r, r.status_code, r.text)
        print(sender_id)
        print(json_data)

    def get_user(self, sender_id):
        # Payload:
        # - gender: (str) eg: male, female
        # - locale: (str) eg: en_US
        # - timezone: (int) eg: -3,
        # - first_name: (str) eg: Clifford
        # - last_name: (str) eg: Burton,
        # - name: (str) Clifford Burton,
        # - profile_pic: (str) https//..,
        # - id: (str) eg: 23455
        uri = 'https://graph.facebook.com/v3.2/{sender_id}'.format(sender_id=sender_id)

        params = {
            "access_token": self.fb_token,
            "fields": 'gender,locale,timezone,first_name,last_name,name,profile_pic'
        }
        r = requests.get(
            uri,
            params=params
        )
        print('-----------------------------USER------------------------------------')
        print(r, r.status_code, r.text)
        print(sender_id)
        print('-----------------------------USER------------------------------------')

        return r.json()

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

    def simple_response(self, sender_id, text):
        """
        Send API Basics https://developers.facebook.com/docs/messenger-platform/send-messages/
        """
        json_data = {
            "recipient": {
                "id": sender_id
            },
            "messaging_type": "response",
            "message": {
                "text": text
            }
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

    def respond(self, sender_id, typeMessage, elements=None, quick_reply=None):
        json_data = {
            "recipient": {"id": sender_id},
            "messaging_type": "response",
            "message": self.get_message(
                elements=elements,
                typeMessage=typeMessage,
                quick_reply=quick_reply
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

    def get_message(self, typeMessage, elements=None, quick_reply=None):
        msg = {}
        if elements and not quick_reply:
            if typeMessage == self.FB_MESSAGE_TYPE_TEMPLATE:
                msg.update({
                    "attachment": {
                        "type": self.FB_MESSAGE_TYPE_TEMPLATE,
                        "payload": {
                            "template_type": self.FB_TEMPLATE_TYPE_GENERIC,
                            "elements": elements
                        }
                    }
                })
        if quick_reply:
            msg.update(quick_reply)
        return msg

    def get_element(self, element_type, **kwargs):
        element = self.ELEMENTS_TYPES.get(element_type, None)
        if element:
            return element().get_element(**kwargs)
        else:
            raise UndefinedElementType(element_type)


class FacebookQuickReplies(object):
        """
            Doc: https://developers.facebook.com/docs/messenger-platform/send-messages/quick-replies
        """

        LOCATION = 'location'
        PHONE = 'user_phone_number'
        EMAIL = 'user_email'
        LIST_OPTIONS = 'list_options'

        QUICK_REPLIES = {
            LOCATION: {
                'text': 'Please share your location:',
                'type': LOCATION,
            },
            PHONE: {
                'text': 'Please share your phone number:',
                'type': PHONE,
            },
            EMAIL: {
                'text': 'Please share your email:',
                'type': EMAIL,
            },
            LIST_OPTIONS: {
                'text': 'Do you want see more?',
            }
        }

        def __init__(self):
            self.list_options = []

        def add_list_options(self, title, payload, image_url=None, content_type='text'):
            self.list_options.append({
                "content_type": content_type,
                "title": title,
                "payload": payload,
                "image_url": image_url
            })

        def get_list_options(self):
            return self.list_options

        def get_quick_reply(self, typeMessage, text=None):
            reply = self.QUICK_REPLIES.get(typeMessage)
            msg = {
                "text": reply.get('text') if not text else text,
                "quick_replies": [
                    {
                        "content_type": reply.get('type')
                    }
                ]
            }
            if typeMessage == self.LIST_OPTIONS:
                msg.update({
                    "text": reply.get('text') if not text else text,
                    "quick_replies": self.list_options
                })
            return msg
