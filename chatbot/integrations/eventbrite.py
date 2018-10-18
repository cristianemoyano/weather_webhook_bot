from chatbot.integrations.base import Integration
from chatbot.constants import EB_ACCESS_TOKEN
import eventbrite
import urllib


class EventbriteIntegration(Integration):
    """docstring for EventbriteIntegration"""
    def __init__(self):
        super(EventbriteIntegration, self).__init__()
        self.EB_EVENTS_ENDPOINT = '/events/search/'
        self.eb_token = EB_ACCESS_TOKEN
        self.is_by_organization = False
        self.ORG_ID = '61565826027'
        self.chatbot_app = 'DialogFlow'
        self.MAP_PARAMETERS = {
            'DialogFlow': {
                'general': [
                    ('location.address', 'geo-city'),
                    ('name_filter', 'event-title'),
                ],
                'by_organization_id': [
                    ('name_filter', 'event-title'),
                ],
            },
        }

    def respond(self, params={}, limit=None):
        get_params = self.map_get_params(params)
        params_encoded = urllib.urlencode(get_params)
        if self.is_by_organization:
            response = self.get_events_by_organization_id(
                params=params_encoded,
                limit=limit,
                org_id=self.ORG_ID
            )
        else:
            response = self.get_events(
                params=params_encoded,
                limit=limit
            )
        return response

    def get_events_by_organization_id(self, params, org_id, limit=None):
        eventbrite_api = self.get_eventbrite_api()
        endpoint = '/organizations/{org_id}/events/'.format(org_id=org_id)
        if params:
            url = endpoint + '?' + params + '&status=live'
        else:
            url = endpoint + '?status=live'
        response = [
            element
            for element in eventbrite_api.get(
                url
            )['events']
        ]
        return response[:limit]

    def get_events(self, params, limit=None):
        eventbrite_api = self.get_eventbrite_api()
        endpoint = self.EB_EVENTS_ENDPOINT
        url = endpoint + '?' + params
        response = [
            element
            for element in eventbrite_api.get(
                url
            )['events']
        ]
        return response[:limit]

    def map_get_params(self, req_params):
        endpoint_type = 'general'
        if self.is_by_organization:
            endpoint_type = 'by_organization_id'
        return {
            key: req_params.get(values)
            for key, values in self.MAP_PARAMETERS[self.chatbot_app].get(endpoint_type)
            if req_params.get(values)
        }

    def get_eventbrite_api(self):
        return eventbrite.Eventbrite(EB_ACCESS_TOKEN)
