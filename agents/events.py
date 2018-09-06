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
        intent = post.get('originalDetectIntentRequest')
        if (intent and events):
            integration = build_integration_by_source(intent.get('source'))
            sender_id = post.get('originalDetectIntentRequest').get('payload').get('data').get('sender').get('id')

            elements = [
                integration.get_element(
                    title=event.get('name').get('text'),
                    sub='Eventbrite',
                    image_url=event.get('logo').get('url'),
                    btn_title='View',
                    btn_url=event.get('url')
                )
                for event in events if events
            ]
            integration.respond(sender_id, elements)

            return {
                "fulfillmentText": 'Message from server.',
                "source": "weather-webhook-bot-app.herokuapp.com/webhook",
            }
        speech = "The event is " + events[0].get('name').get('text')
        return {
            "fulfillmentText": speech,
            "source": "weather-webhook-bot-app.herokuapp.com/webhook",
        }
