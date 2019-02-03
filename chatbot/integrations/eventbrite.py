from chatbot.integrations.base import Integration
from chatbot.constants import DEBUG
from chatbot.constants import (
    EB_ACCESS_TOKEN,
    EB_ORGANIZATION_ID,
    EB_IS_BY_ORGANIZATION,
)
import eventbrite
import urllib


EB_WIDGETS_QA = "https://www.evbqa.com/static/widgets/eb_widgets.js"
EB_WIDGETS_PROD = "https://www.eventbrite.com/static/widgets/eb_widgets.js"


def get_widgets():
    return EB_WIDGETS_QA if DEBUG else EB_WIDGETS_PROD


class EventbriteIntegration(Integration):
    """docstring for EventbriteIntegration"""
    def __init__(self):
        super(EventbriteIntegration, self).__init__()
        self.EB_EVENTS_ENDPOINT = '/events/search/'
        self.EB_EVENTS_ENDPOINT_BY_ID = '/events/'
        self.eb_token = EB_ACCESS_TOKEN
        self.is_by_organization = EB_IS_BY_ORGANIZATION
        self.ORG_ID = EB_ORGANIZATION_ID
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
        params_encoded = urllib.parse.urlencode(get_params)
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
        request = eventbrite_api.get(url).get('events')
        if request:
            response = [
                event
                for event in request
            ]
            return response[:limit]
        else:
            url = endpoint + '?status=live'
            request = eventbrite_api.get(url).get('events')
            if request:
                response = [
                    event
                    for event in request
                ]
                return response[:limit]

    def get_events(self, params, limit=None):
        eventbrite_api = self.get_eventbrite_api()
        endpoint = self.EB_EVENTS_ENDPOINT
        url = endpoint + '?' + params
        request = eventbrite_api.get(url).get('events')
        if request:
            response = [
                event
                for event in request
            ]
            return response[:limit]

    def get_event_by_id(self, event_id):
        eventbrite_api = self.get_eventbrite_api()
        endpoint = self.EB_EVENTS_ENDPOINT_BY_ID
        url = endpoint + event_id
        response = eventbrite_api.get(url)
        return response

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


def get_logo(event):
    logo = event.get('logo')
    logo_url = ''
    if logo:
        logo_url = logo.get('url')
    return logo_url


def get_events_data(events):
        events_data = []
        if events:
            for event in events:
                events_data.append({
                    'title': event.get('name').get('text'),
                    'image_url': get_logo(event),
                    'url': event.get('url'),
                    'id': event.get('id'),
                })
        return events_data
