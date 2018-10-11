from chatbot.agents.base import Agent
from chatbot.integrations.builder import build_integration_by_source
from chatbot.integrations.facebook import FB_SENDER_ACTIONS


class EventAgent(Agent):
    """Agent that processes events"""

    MAP_PARAMETERS = [
        ('location.address', 'geo-city'),
    ]

    def __init__(self):
        super(EventAgent, self).__init__()
        self.event_integration = 'eventbrite'

    def process_request(self, post):
        print(post)
        req_params = post.get('queryResult').get('parameters')
        get_params = {key: req_params.get(values) for key, values in self.MAP_PARAMETERS}
        event_integration = build_integration_by_source(self.event_integration)
        events = event_integration.respond(
            endpoint='/events/search/',
            target='events',
            params=get_params,
            limit=3,
        )
        events_data = self.get_events_data(events)
        intent = post.get('originalDetectIntentRequest')
        if (intent.get('payload') and events):
            integration = build_integration_by_source(intent.get('source'))
            sender_id = post.get('originalDetectIntentRequest').get('payload').get('data').get('sender').get('id')
            integration.display_sender_action(sender_id, FB_SENDER_ACTIONS.get('typing_on'))
            elements = [
                integration.get_element(
                    element_type='simple',
                    title=event.get('title'),
                    sub='Eventbrite',
                    image_url=event.get('image_url'),
                    btn_title='View',
                    webview='https://weather-webhook-bot-app.herokuapp.com/webview?eid=' + event.get('id'),
                    btn_url=event.get('url')
                )
                for event in events_data
            ]
            integration.respond(sender_id, 'template', elements)
            integration.respond(sender_id, 'list_options', is_quick_reply=True)
            # integration.respond(sender_id, None, 'location')
            # integration.respond(sender_id, None, 'phone_number')
            # integration.respond(sender_id, None, 'email')
            integration.display_sender_action(sender_id, FB_SENDER_ACTIONS.get('typing_off'))
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
