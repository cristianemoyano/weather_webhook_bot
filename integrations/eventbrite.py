from integrations.base import Integration
from constants import EB_ACCESS_TOKEN
from eventbrite import Eventbrite
import urllib


class EventbriteIntegration(Integration):
    """docstring for EventbriteIntegration"""
    def __init__(self):
        super(EventbriteIntegration, self).__init__()
        self.eb_token = EB_ACCESS_TOKEN

    def respond(self, endpoint, target, params={}):
        params_encoded = urllib.parse.urlencode(params)
        url = endpoint + '?' + params_encoded
        eventbrite = Eventbrite(EB_ACCESS_TOKEN)
        response = [
            element
            for element in eventbrite.get(
                url
            )[target]
        ]
        return response
