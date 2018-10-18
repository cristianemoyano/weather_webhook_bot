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


class EventAgent(Agent):
    """Agent that processes events"""

    def __init__(self):
        super(EventAgent, self).__init__()
        self.event_integration = EB_INTEGRATION

    def process_request(self, post):
        print(post)
        req_params = post.get('queryResult').get('parameters')
        event_integration = build_integration_by_source(self.event_integration)
        event_integration.is_by_organization = True
        events = event_integration.respond(
            params=req_params,
            limit=3,
        )
        events_data = self.get_events_data(events)
        intent = post.get('originalDetectIntentRequest')
        if (intent.get('payload') and events and intent.get('source') == FB_INTEGRATION):
            # Build FB integration
            integration = build_integration_by_source(intent.get('source'))
            # get sender_id for respond
            sender_id = post.get('originalDetectIntentRequest').get('payload').get('data').get('sender').get('id')
            # turn on typing in messenger
            integration.display_sender_action(sender_id, FB_SENDER_ACTIONS.get('typing_on'))
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
            fb_simple_element.add_postback_button(
                btn_title='more events',
                btn_payload='more events'
            )
            # create a specific element with events for messenger
            webview_url = '{url}{event_param}'.format(url=self.request_url, event_param='?eid=')
            elements = [
                integration.get_element(
                    element_type=integration.ELEMENTS_TYPE.get('simple'),
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
        events_data = events_data[0].get('title') if events_data else ''
        speech = "I found this event in " + req_params.get('geo-city') + ': ' + events_data
        return {
            "fulfillmentText": speech,
            "source": "weather-webhook-bot-app.herokuapp.com/webhook",
        }

    def get_events_data(self, events):
        events_data = []
        if events:
            for event in events:
                logo = event.get('logo')
                logo_url = ''
                if logo:
                    logo_url = logo.get('url')
                events_data.append({
                    'title': event.get('name').get('text'),
                    'image_url': logo_url,
                    'url': event.get('url'),
                    'id': event.get('id'),
                })
        return events_data
