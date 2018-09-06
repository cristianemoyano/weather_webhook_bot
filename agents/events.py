import requests

from agents.base import Agent
from eventbrite import Eventbrite
from constants import EB_ACCESS_TOKEN, FB_MESSENGER_ACCESS_TOKEN


class EventAgent(Agent):
    """Agent that processes events"""

    def __init__(self):
        super(EventAgent, self).__init__()

    def process(self, post):
        print(post)
        intent = post.get('originalDetectIntentRequest')
        if (intent and intent.get('source') == 'facebook'):
            sender_id = post.get('originalDetectIntentRequest').get('payload').get('data').get('sender').get('id')
            msg = {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "elements": [
                            {
                                "title": "Hello 1",
                                "subtitle": "Subtitle 1",
                                "buttons": [{
                                    "title": "View",
                                    "type": "web_url",
                                    "url": "https://www.medium.com/",
                                    "messenger_extensions": "false",
                                    "webview_height_ratio": "full"
                                }],
                                "default_action": {
                                    "type": "web_url",
                                    "url": "https://www.medium.com/",
                                    "messenger_extensions": "false",
                                    "webview_height_ratio": "full"
                                }
                            },
                            {
                                "title": "Hello 2",
                                "subtitle": "Subtitle 2",
                                "image_url": "https://cdn-images-1.medium.com/1*Vkf6A8Mb0wBoL3Fw1u0paA.jpeg",
                                "buttons": [{
                                    "title": "View",
                                    "type": "web_url",
                                    "url": "https://www.medium.com/",
                                    "messenger_extensions": "false",
                                    "webview_height_ratio": "full"
                                }],
                                "default_action": {
                                    "type": "web_url",
                                    "url": "https://www.medium.com/",
                                    "messenger_extensions": "false",
                                    "webview_height_ratio": "full"
                                }
                            }
                        ]
                    }
                }
            }
            json_data = {
                "recipient": {"id": sender_id},
                "message": msg
            }

            params = {
                "access_token": FB_MESSENGER_ACCESS_TOKEN
            }
            r = requests.post(
                'https://graph.facebook.com/v2.6/me/messages',
                json=json_data,
                params=params
            )
            print(r, r.status_code, r.text)
            print(sender_id)
            print(json_data)

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
