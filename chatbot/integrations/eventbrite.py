from chatbot.integrations.base import Integration
from chatbot.constants import EB_ACCESS_TOKEN
import eventbrite
import urllib


class EventbriteIntegration(Integration):
    """docstring for EventbriteIntegration"""
    def __init__(self):
        super(EventbriteIntegration, self).__init__()
        self.EB_EVENTS_ENDPOINT_BY_ORG = 'organizations/61565826027/events/'
        self.EB_EVENTS_ENDPOINT = '/events/search/'
        self.eb_token = EB_ACCESS_TOKEN
        self.MAP_PARAMETERS = {
            'DialogFlow': [
                ('location.address', 'geo-city'),
                ('name_filter', 'event-title'),
            ]
        }

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

    def map_get_params(self, req_params, app='DialogFlow'):
        return {key: req_params.get(values) for key, values in self.MAP_PARAMETERS[app]}
