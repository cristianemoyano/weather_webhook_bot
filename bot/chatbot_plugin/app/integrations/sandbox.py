

WELCOME_ACTION = 'welcome_action'
SIMPLE_FB_MSG_ACTION = 'simple_fb_msg_action'
BLANK_ACTION = 'blank_action'
CUSTOM_EVENT_ID = 'custom_event_id'

CONTEXT_ACTIONS = [
    {
        'id': SIMPLE_FB_MSG_ACTION,
        'label': 'Simple Facebook Message',
    },
    {
        'id': WELCOME_ACTION,
        'label': 'Welcome Message',
    },
    {
        'id': CUSTOM_EVENT_ID,
        'label': 'Custom Event ID',
    }
]


def get_custom_event_post_example(
        sender_id,
        event_id,
        source='facebook',
        lang_code='en',
        agent='CustomEventSearch',
        organizer_id='1234'
):
    return {
        'event_id': event_id,
        'source': source,
        'lang_code': lang_code,
        'agent': agent,
        'sender_id': sender_id,
        'organizer_id': organizer_id,
    }


def get_facebook_welcome_payload(sender_id, recipient_id, language_code='en'):
    return {
        'responseId': '435bada8-a660-43e8-9cfb-5f8bab04754b',
        'queryResult': {
            'queryText': 'FACEBOOK_WELCOME',
            'action': 'input.welcome',
            'parameters': {'get_started': '1'},
            'allRequiredParamsPresent': True,
            'fulfillmentText': 'Hello!',
            'fulfillmentMessages': [
                {
                    'text': {
                        'text': ['']
                    },
                    'platform': 'FACEBOOK'
                },
                {
                    'text': {'text': ['Hello!']}
                }
            ],
            'outputContexts': [
                {
                    'name': 'projects/events-search-1-90a32/agent/sessions//contexts/facebook_welcome',
                    'parameters': {
                        'get_started.original': '',
                        'get_started': '1'
                    }
                },
                {
                    'name': 'projects/events-search-1-90a32/agent/sessions//contexts/generic',
                    'lifespanCount': 4,
                    'parameters':
                        {
                            'get_started.original': '',
                            'get_started': '1',
                            'facebook_sender_id': '2093633150674633'
                        }
                }
            ],
            'intent': {
                'name': 'projects/events-search-1-90a32/agent/intents/1aa662bd-785d-4ba4-a7f2-54921aaea726',
                'displayName': 'DefaultWelcomeIntent'
            },
            'intentDetectionConfidence': 1.0,
            'languageCode': language_code
        },
        'originalDetectIntentRequest': {
            'source': 'facebook',
            'payload': {
                'data': {
                    'postback': {
                        'payload': 'FACEBOOK_WELCOME',
                        'title': 'Empezar'
                    },
                    'sender': {
                        'id': sender_id
                    },
                    'recipient': {
                        'id': recipient_id
                    },
                    'timestamp': 1543761659381.0
                },
                'source': 'facebook'
            }
        },
        'session': 'projects/events-search-1-90a32/agent/sessions/f9e36b06-ecdd-4041-8209-7933c2183071'
    }
