from agents.base import Agent
from eventbrite import Eventbrite
from constants import EB_ACCESS_TOKEN


class EventAgent(Agent):
    """Agent that processes events"""
    def __init__(self):
        super(EventAgent, self).__init__()

    def process(self, post):
        print(post)
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
