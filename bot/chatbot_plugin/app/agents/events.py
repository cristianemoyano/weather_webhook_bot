from .base import Agent
from .decorators import has_required_params
from ..integrations.builder import (
    FB_INTEGRATION,
    EB_INTEGRATION,
    build_integration_by_source,
)
from ..integrations.facebook import (
    FB_SENDER_ACTIONS,
    FacebookQuickReplies,
    FacebookSimpleElement,
)
from ..integrations.eventbrite import (
    get_events_data,
    get_logo,
)
from ..utils import (
    get_text,
)


class EventAgent(Agent):
    """Agent that processes events"""

    def __init__(self):
        super(EventAgent, self).__init__()
        self.event_integration = build_integration_by_source(EB_INTEGRATION)
        self.messenger_integration = build_integration_by_source(FB_INTEGRATION)

    def process_request(self, post):
        print(post)
        try:
            req_params = post.get('queryResult').get('parameters')
        except Exception:
            return None

        events = self.event_integration.respond(
            params=req_params,
            limit=3,
        )
        print(events)
        events_data = get_events_data(events)
        intent = post.get('originalDetectIntentRequest')
        if (intent.get('payload') and events and intent.get('source') == FB_INTEGRATION):
            # get sender_id to respond
            sender_id = self.messenger_integration.get_sender_id(post)
            # Get user
            user = self.messenger_integration.get_user(sender_id)
            # Send greeting to the user
            text = "{user_first_name} according to your search, I've found these events:".format(
                user_first_name=user.get('first_name')
            )
            self.messenger_integration.simple_response(sender_id, text)
            # turn on typing in messenger
            self.messenger_integration.send_typing_on(sender_id)
            # create buttons
            fb_simple_element = FacebookSimpleElement()
            fb_simple_element.add_button(
                btn_title="View",
                btn_type=fb_simple_element.BTN_TYPE_WEB_URL,
                msg_extension=fb_simple_element.MSG_EXTENSION_FALSE,
                webview_height=fb_simple_element.WEBVIEW_HEIGHT_RATIO_MEDIUM
            )
            fb_simple_element.add_button(
                btn_title="Tickets",
                btn_type=fb_simple_element.BTN_TYPE_WEB_URL,
                msg_extension=fb_simple_element.MSG_EXTENSION_TRUE,
                webview_height=fb_simple_element.WEBVIEW_HEIGHT_RATIO_LARGE
            )

            url = 'https://{root}/webview'.format(root=self.request_url.split('/')[2])
            webview_url = '{url}{event_param}'.format(url=url, event_param='?eid=')
            elements = [
                self.messenger_integration.get_element(
                    element_type=self.messenger_integration.ELEMENTS_TYPE_SIMPLE,
                    title=event.get('title'),
                    subtitle='Eventbrite',
                    image_url=event.get('image_url'),
                    btn_title='View',
                    webview='{webview_url}{eid}'.format(webview_url=webview_url, eid=event.get('id')),
                    buttons=fb_simple_element.buttons,
                    btn_url=event.get('url'),
                    msg_extension=fb_simple_element.MSG_EXTENSION_FALSE,
                    webview_height_ratio=fb_simple_element.WEBVIEW_HEIGHT_RATIO_LARGE
                )
                for event in events_data
            ]
            # send element created on messenger
            self.messenger_integration.respond(
                sender_id=sender_id,
                typeMessage=self.messenger_integration.FB_MESSAGE_TYPE_TEMPLATE,
                elements=elements
            )
            # create and respond a quick reply
            quick_reply = FacebookQuickReplies()
            quick_reply.add_list_options(title='Yes, more !', payload='more events')
            quick_reply.add_list_options(title='No, thanks!', payload='thank you')
            self.messenger_integration.respond(
                sender_id=sender_id,
                typeMessage=quick_reply.LIST_OPTIONS,
                quick_reply=quick_reply.get_quick_reply(quick_reply.LIST_OPTIONS)
            )
            # turn off the typing on messenger
            self.messenger_integration.display_sender_action(sender_id, FB_SENDER_ACTIONS.get('typing_off'))
            # response for chatbot app
            return {
                # "fulfillmentText": 'Message from server.',
                "source": "weather-webhook-bot-app.herokuapp.com/webhook",
            }
        if events_data:
            events_data = events_data[0].get('title') if events_data else ''
            speech = "I found this event in " + req_params.get('geo-city') + ': ' + events_data
        else:
            speech = "Sorry I have not found any event :("
        return {
            "fulfillmentText": speech,
            "source": "weather-webhook-bot-app.herokuapp.com/webhook",
        }


class CustomEventAgent(Agent):
    """Agent that processes events"""

    def __init__(self):
        super(CustomEventAgent, self).__init__()
        self.event_integration = build_integration_by_source(EB_INTEGRATION)
        self.messenger_integration = build_integration_by_source(FB_INTEGRATION)
        self.required_params = [
            'event_id',
            'source',
            'lang_code',
            'agent',
            'sender_id',
            'organizer_id'
        ]

    @has_required_params
    def process_request(self, post):
        print(post)
        event_id = post.get('event_id')
        sender_id = post.get('sender_id')
        event = self.event_integration.get_event_by_id(event_id)
        print(event)
        if (event.ok and post.get('source') == FB_INTEGRATION):
            # turn on typing in messenger
            self.messenger_integration.send_typing_on(sender_id)
            # create buttons
            fb_simple_element = FacebookSimpleElement()
            fb_simple_element.add_button(
                btn_title="View",
                btn_type=fb_simple_element.BTN_TYPE_WEB_URL,
                msg_extension=fb_simple_element.MSG_EXTENSION_FALSE,
                webview_height=fb_simple_element.WEBVIEW_HEIGHT_RATIO_MEDIUM
            )
            fb_simple_element.add_button(
                btn_title="Tickets",
                btn_type=fb_simple_element.BTN_TYPE_WEB_URL,
                msg_extension=fb_simple_element.MSG_EXTENSION_TRUE,
                webview_height=fb_simple_element.WEBVIEW_HEIGHT_RATIO_LARGE
            )

            url = 'https://{root}/webview'.format(root=self.request_url.split('/')[2])
            webview_url = '{url}{event_param}'.format(url=url, event_param='?eid=')

            elements = [
                self.messenger_integration.get_element(
                    element_type=self.messenger_integration.ELEMENTS_TYPE_SIMPLE,
                    title=event.get('name').get('text') or event.get('name'),
                    subtitle='Eventbrite',
                    image_url=get_logo(event),
                    btn_title='View',
                    webview='{webview_url}{eid}'.format(webview_url=webview_url, eid=event.get('id')),
                    buttons=fb_simple_element.buttons,
                    btn_url=event.get('url'),
                    msg_extension=fb_simple_element.MSG_EXTENSION_FALSE,
                    webview_height_ratio=fb_simple_element.WEBVIEW_HEIGHT_RATIO_LARGE
                )
            ]

            # send element created on messenger
            self.messenger_integration.respond(
                sender_id=sender_id,
                typeMessage=self.messenger_integration.FB_MESSAGE_TYPE_TEMPLATE,
                elements=elements
            )
            return {
                'response': 'ok'
            }
        return {
            'response': 'error'
        }


class GetEventByIdAgent(Agent):
    """Agent that processes events"""

    def __init__(self):
        super(GetEventByIdAgent, self).__init__()
        self.event_integration = build_integration_by_source(EB_INTEGRATION)
        self.messenger_integration = build_integration_by_source(FB_INTEGRATION)
        self.required_params = [
            'event_id',
            'agent',
        ]

    @has_required_params
    def process_request(self, post):
        print(post)
        event_id = post.get('event_id')
        lang_code = post.get('lang_code', 'en')
        expand = post.get('expand', False)
        event = self.event_integration.get_event_by_id(event_id)
        print(event)
        if (event.ok):
            url = 'https://{root}/webview'.format(root=self.request_url.split('/')[2])
            webview_url = '{url}{event_param}'.format(url=url, event_param='?eid=')
            response = {
                'embedded_checkout': '{webview_url}{eid}'.format(webview_url=webview_url, eid=event.get('id')),
                'event_logo': get_logo(event),
                'event_title': event.get('name').get('text'),
                'powered_by': 'Eventbrite',
                'btn_title': get_text(lang_code, 'View'),
                'event_url': event.get('url'),
            }
            if bool(int(expand)):
                response.update({'event_data_expanded': event})
            return response
        return {
            'response': 'error'
        }


class GetWebviewAgent(Agent):
    """Agent that processes events"""

    def __init__(self):
        super(GetWebviewAgent, self).__init__()
        self.event_integration = build_integration_by_source(EB_INTEGRATION)
        self.required_params = [
            'event_id',
            'agent',
            'user_id'
        ]

    @has_required_params
    def process_request(self, post):
        print(post)
        sender_id = post.get('user_id')
        event_id = post.get('event_id')
        event = self.event_integration.get_event_by_id(event_id)
        print(event)
        if (event.ok):
            url = 'https://{root}/webview'.format(root=self.request_url.split('/')[2])
            webview_url = '{url}{event_param}'.format(url=url, event_param='?eid=')
            display_url = '{webview_url}{eid}'.format(webview_url=webview_url, eid=event.get('id'))
            event_logo = get_logo(event)
            event_url = event.get('url')
            event_title = event.get('name').get('text')
            template = self.get_template(
                webview_url=display_url,
                image_url=event_logo,
                event_url=event_url,
                event_title=event_title
            )
            # send element created on messenger
            self.messenger_integration.direct_response(
                sender_id=sender_id,
                dict_message=template
            )
            return 'ok'
        return {
            'response': 'error'
        }

    def get_template(self, webview_url, image_url, event_url, event_title):
        return {
            'messages':
            [
                {
                    'attachment':
                    {
                        'type': 'template',
                        'payload':
                        {
                            'template_type': 'generic',
                            'elements':
                            [
                                {
                                    'title': event_title,
                                    'subtitle': 'Eventbrite',
                                    'image_url': image_url,
                                    'buttons':
                                    [
                                        {
                                            'type': 'web_url',
                                            'url': event_url,
                                            'title': 'View',
                                            'messenger_extensions': 'false',
                                            'webview_height_ratio': 'tall'
                                        },
                                        {
                                            'type': 'web_url',
                                            'url': webview_url,
                                            'title': 'Tickets',
                                            'messenger_extensions': 'true',
                                            'webview_height_ratio': 'full'
                                        }
                                    ],
                                    'default_action': {
                                        "type": 'web_url',
                                        "url": event_url,
                                        "messenger_extensions": 'false',
                                        "webview_height_ratio": 'tall',
                                    },
                                }
                            ]
                        }
                    }
                }
            ]
        }
