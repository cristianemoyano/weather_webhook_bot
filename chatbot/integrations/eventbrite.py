from chatbot.integrations.base import Integration
from chatbot.constants import EB_ACCESS_TOKEN
import eventbrite
import urllib


class EventbriteIntegration(Integration):
    """docstring for EventbriteIntegration"""
    def __init__(self):
        super(EventbriteIntegration, self).__init__()
        self.eb_token = EB_ACCESS_TOKEN

    def respond(self, endpoint, target, params={}, limit=None):
        params_encoded = urllib.parse.urlencode(params)
        url = endpoint + '?' + params_encoded
        eventbrite_api = eventbrite.Eventbrite(EB_ACCESS_TOKEN)
        response = [
            element
            for element in eventbrite_api.get(
                url
            )[target]
        ]
        return response[:limit]
