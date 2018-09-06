from agents.base import Agent
from eventbrite import Eventbrite
from constants import EB_ACCESS_TOKEN
from integrations.builder import build_integration_by_source


class EventAgent(Agent):
    """Agent that processes events"""

    def __init__(self):
        super(EventAgent, self).__init__()

    def process(self, post):
        print(post)
        intent = post.get('originalDetectIntentRequest')
        if (intent):
            integration = build_integration_by_source(intent.get('source'))
            sender_id = post.get('originalDetectIntentRequest').get('payload').get('data').get('sender').get('id')
            integration.respond(sender_id)

            return {
                "fulfillmentText": 'Message from server.',
                "source": "weather-webhook-bot-app.herokuapp.com/webhook",
            }
        eventbrite = Eventbrite(EB_ACCESS_TOKEN)
        events = [
            event
            for event in eventbrite.get(
                '/events/search/'
            )['events']
        ]
        event = events[0]
        speech = "The event is " + event.get('name').get('text')
        return {
            "fulfillmentText": speech,
            "source": "weather-webhook-bot-app.herokuapp.com/webhook",
        }
