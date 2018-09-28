from agents.base import Agent
from integrations.builder import build_integration_by_source


class EventAgent(Agent):
    """Agent that processes events"""

    MAP_PARAMETERS = [
        ('location.address', 'geo-city'),
    ]

    def __init__(self):
        super(EventAgent, self).__init__()
        self.event_integration = 'eventbrite'

    def process(self, post):
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

            elements = [
                integration.get_element(
                    element_type='simple',
                    title=event.get('title'),
                    sub='Eventbrite',
                    image_url=event.get('image_url'),
                    btn_title='View',
                    webview='https://weather-webhook-bot-app.herokuapp.com/webview',
                    btn_url=event.get('url')
                )
                for event in events_data
            ]
            integration.respond(sender_id, elements, 'template')
            integration.respond(sender_id, None, 'quick_replies')
            return {
                # "fulfillmentText": 'Message from server.',
                "source": "weather-webhook-bot-app.herokuapp.com/webhook",
            }
        speech = "I found this event in " + req_params.get('geo-city') + ': ' + events_data[0].get('title')
        return {
            "fulfillmentText": speech,
            "source": "weather-webhook-bot-app.herokuapp.com/webhook",
        }

    def get_events_data(self, events):
        events_data = []
        for event in events:
            logo = event.get('logo')
            logo_url = ''
            if logo:
                logo_url = logo.get('url')
            events_data.append({
                'title': event.get('name').get('text'),
                'image_url': logo_url,
                'url': event.get('url')
            })
        return events_data
