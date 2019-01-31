from chatbot.utils import (
    get_logger,
    LOG_AGENT_DIR,
    get_text,
)
from chatbot.agents.base import Agent
from chatbot.integrations.builder import (
    FB_INTEGRATION,
    EB_INTEGRATION,
    build_integration_by_source,
)
from chatbot.integrations.facebook import (
    FB_SENDER_ACTIONS,
    FacebookQuickReplies,
    FacebookSimpleElement,
)
from chatbot.integrations.eventbrite import get_events_data


def _get_gretting_text(user_first_name, lang_out):
    start_phrase = 'Hey'
    last_phrase = 'I recommend these events!'
    text = get_text(lang_out, start_phrase) + ' ' + user_first_name + ', ' + get_text(lang_out, last_phrase)
    return text


class WelcomeAgent(Agent):
    """Agent that processes events"""
    def __init__(self):
        super(WelcomeAgent, self).__init__()
        self.logger = get_logger('welcome_agent', LOG_AGENT_DIR)
        self.event_integration = build_integration_by_source(EB_INTEGRATION)
        self.messenger_integration = build_integration_by_source(FB_INTEGRATION)

    def get_source(self):
        try:
            source = '{url}/webhook'.format(url=self.request_url.split('/')[2])
        except IndexError:
            source = ''
        return source

    def process_request(self, post):
        self.logger.info(post)
        self.logger.info(self.lang_code)
        intent = post.get('originalDetectIntentRequest')
        # get sender_id
        sender_id = self.messenger_integration.get_sender_id(post)
        # send typing on
        self.messenger_integration.send_typing_on(sender_id)
        # get events
        events = self.event_integration.respond(
            limit=3,
        )
        self.logger.info(events)
        events_data = get_events_data(events)
        payload = post.get('queryResult').get('queryText')
        if (
            intent.get('payload') and
            events and
            intent.get('source') == FB_INTEGRATION and
            payload == 'FACEBOOK_WELCOME'
        ):
            # Get user
            user = self.messenger_integration.get_user(sender_id)
            # Send greeting to the user
            text = _get_gretting_text(user.get('first_name'), self.lang_code)
            self.messenger_integration.simple_response(sender_id, get_text(self.lang_code, text))
            # create buttons
            fb_simple_element = FacebookSimpleElement()
            fb_simple_element.add_button(
                btn_title=get_text(self.lang_code, 'See event'),
                btn_type=fb_simple_element.BTN_TYPE_WEB_URL,
                msg_extension=fb_simple_element.MSG_EXTENSION_FALSE,
                webview_height=fb_simple_element.WEBVIEW_HEIGHT_RATIO_MEDIUM
            )
            fb_simple_element.add_button(
                btn_title=get_text(self.lang_code, 'Tickets'),
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
                    btn_title=get_text(self.lang_code, 'See event'),
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
            quick_reply.add_list_options(
                title=get_text(self.lang_code, 'Yes, more !'),
                payload=get_text(self.lang_code, 'more events')
            )
            quick_reply.add_list_options(
                title=get_text(self.lang_code, 'No, thanks!'),
                payload=get_text(self.lang_code, 'thank you')
            )
            self.messenger_integration.respond(
                sender_id=sender_id,
                typeMessage=quick_reply.LIST_OPTIONS,
                quick_reply=quick_reply.get_quick_reply(quick_reply.LIST_OPTIONS)
            )
            # turn off the typing on messenger
            self.messenger_integration.display_sender_action(sender_id, FB_SENDER_ACTIONS.get('typing_off'))
            # response for chatbot app
            return {
                'source': self.get_source(),
            }
        if events_data:
            events_data = events_data[0].get('title') if events_data else ''
            speech = get_text(self.lang_code, 'I found this event for you: ') + events_data
        else:
            speech = get_text(self.lang_code, 'Sorry I have not found any event :(')
        return {
            'fulfillmentText': speech,
            'source': self.get_source(),
        }
