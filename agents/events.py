from agents.base import Agent
from eventbrite import Eventbrite
from constants import EB_ACCESS_TOKEN


class EventAgent(Agent):
    """Agent that processes events"""

    def __init__(self):
        super(EventAgent, self).__init__()

    def process(self, post):
        print(post)
        intent = post.get('originalDetectIntentRequest')
        if (intent and intent.get('source') == 'facebook'):
            sender_id = post.get('originalDetectIntentRequest').get('payload').get('data').get('sender').get('id')
            messageData = {
                'recipient': {
                    'id': sender_id
                },
                'message': {
                    'attachment': {
                        'type': "template",
                        'payload': {
                            'template_type': 'generic',
                            'elements':
                                [{
                                    'title': 'Biking',
                                    'subtitle': 'Bike trail',
                                    'item_url': 'https://www.evbqa.com/e/bike-trip-tickets-37353734024',
                                    'image_url':
                                        (
                                            'http://images.singletracks.com/blog/wp-content/uploads/'
                                            '2014/05/Copper-Harbor-copperhippie.jpg'
                                        ),
                                    'buttons':
                                        [
                                            {
                                                'type': 'payment',
                                                'title': 'buy',
                                                'payload': 'ticket_type_vip',
                                                'payment_summary': {
                                                    'currency': 'USD',
                                                    'payment_type': 'FIXED_AMOUNT',
                                                    'is_test_payment': True,
                                                    'merchant_name': 'Eventbrite',
                                                    'requested_user_info': [
                                                        'contact_email'
                                                    ],
                                                    'price_list':[
                                                        {
                                                            'label': 'Subtotal',
                                                            'amount': '1.00'
                                                        }
                                                    ]
                                                }
                                            },
                                            {
                                                'title': '$100 Get tickets',
                                                'type': 'web_url',
                                                'url': 'https://mulberry-surf.glitch.me/webview',
                                                'webview_height_ratio': 'tall',
                                                'messenger_extensions': True,
                                            }
                                        ],
                                }, {
                                    'title': 'dev day',
                                    'subtitle': 'Argentina Dev day',
                                    'item_url':
                                        (
                                            'https://www.eventbrite.com.ar/e/argentina-devday-mendoza-'
                                            'tickets-31298217812?aff=ehomecard'
                                        ),
                                    'image_url':
                                        (
                                            'https://img.evbuc.com/https%3A%2F%2Fcdn.evbuc.com%2Fimages%2F'
                                            '31809526%2F199503150352%2F1%2Foriginal.jpg?w=800&rect=0%2C28%2'
                                            'C960%2C480&s=82345a2d2fba82b996cba87955ef5d23'
                                        ),
                                    'buttons': [{
                                        'type': 'web_url',
                                        'url':
                                            (
                                                'https://www.eventbrite.com.ar/e/argentina-devday-mendoza'
                                                '-tickets-31298217812?aff=ehomecard'
                                            ),
                                        'title': 'Open Web URL'
                                    }, {
                                        'type': 'postback',
                                        'title': 'Call Postback',
                                        'payload': 'Payload for second bubble',
                                    }]
                                }]
                        }
                    }
                }
            }
            return messageData
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
