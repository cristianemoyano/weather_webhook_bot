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


def send_typing_on(intent, post):
    if (intent.get('source') == FB_INTEGRATION):
        # Build FB integration
        integration = build_integration_by_source(intent.get('source'))
        # get sender_id for respond
        sender_id = post.get('originalDetectIntentRequest').get('payload').get('data').get('sender').get('id')
        # turn on typing in messenger
        integration.display_sender_action(sender_id, FB_SENDER_ACTIONS.get('typing_on'))


class WelcomeAgent(Agent):
    """Agent that processes events"""
    def __init__(self):
        super(WelcomeAgent, self).__init__()
        self.event_integration = EB_INTEGRATION

    def process_request(self, post):
        print(post)
        intent = post.get('originalDetectIntentRequest')
        send_typing_on(intent, post)
        event_integration = build_integration_by_source(self.event_integration)
        events = event_integration.respond(
            limit=3,
        )
        print(events)
        events_data = get_events_data(events)
        payload = post.get('queryResult').get('queryText')
        if (
            intent.get('payload') and
            events and
            intent.get('source') == FB_INTEGRATION and
            payload == 'FACEBOOK_WELCOME'
        ):
            # Build FB integration
            integration = build_integration_by_source(intent.get('source'))
            # get sender_id for respond
            sender_id = post.get('originalDetectIntentRequest').get('payload').get('data').get('sender').get('id')
            # Get user
            user = integration.get_user(sender_id)
            # Send greeting to the user
            text = "Hey {user_first_name}, I recommend these events!".format(user_first_name=user.get('first_name'))
            integration.simple_response(sender_id, text)
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
                integration.get_element(
                    element_type=integration.ELEMENTS_TYPE_SIMPLE,
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
            integration.respond(
                sender_id=sender_id,
                typeMessage=integration.FB_MESSAGE_TYPE_TEMPLATE,
                elements=elements
            )
            # create and respond a quick reply
            quick_reply = FacebookQuickReplies()
            quick_reply.add_list_options(title='Yes, more !', payload='more events')
            quick_reply.add_list_options(title='No, thanks!', payload='thank you')
            integration.respond(
                sender_id=sender_id,
                typeMessage=quick_reply.LIST_OPTIONS,
                quick_reply=quick_reply.get_quick_reply(quick_reply.LIST_OPTIONS)
            )
            # turn off the typing on messenger
            integration.display_sender_action(sender_id, FB_SENDER_ACTIONS.get('typing_off'))
            # response for chatbot app
            return {
                # "fulfillmentText": 'Message from server.',
                "source": "weather-webhook-bot-app.herokuapp.com/webhook",
            }
        if events_data:
            events_data = events_data[0].get('title') if events_data else ''
            speech = "I found this event for you: " + events_data
        else:
            speech = "Sorry I have not found any event :("
        return {
            "fulfillmentText": speech,
            "source": "weather-webhook-bot-app.herokuapp.com/webhook",
        }