from chatbot.agents.base import Agent
from chatbot.constants import DEBUG
from chatbot.agents.welcome import WelcomeAgent
from chatbot.agents.events import CustomEventAgent
from chatbot.integrations.sandbox import (
    get_facebook_welcome_payload,
    get_custom_event_post_example,
    WELCOME_ACTION,
    SIMPLE_FB_MSG_ACTION,
    CUSTOM_EVENT_ID,
    BLANK_ACTION
)


class SandBoxAgent(Agent):
    """Agent for testing proposes"""
    def __init__(self):
        super(SandBoxAgent, self).__init__()
        self.language_code = 'es'
        self.welcome_agent = WelcomeAgent()
        self.welcome_agent.request_url = 'localhost'
        self.welcome_agent.lang_code = self.language_code

        self.custom_evt_agent = CustomEventAgent()
        self.custom_evt_agent.request_url = 'localhost/other/other'
        self.custom_evt_agent.lang_code = 'en'
        self.is_debug = DEBUG

    def process_request(self, post):
        if self.is_debug:
            print('-----------------SANDBOX------------------')
            print(post)
            print('-----------------SANDBOX------------------')
            action = post.get('action')
            sender_id = post.get('sender_id', None)
            event_id = post.get('event_id', None)
            if action == WELCOME_ACTION:
                request = get_facebook_welcome_payload(
                    sender_id=post.get('sender_id', '2093633150674633'),
                    recipient_id=post.get('recipient_id', '256171418366507'),
                    language_code=self.language_code
                )
                print(request)
                self.welcome_agent.process_request(request)
            elif action == SIMPLE_FB_MSG_ACTION:
                print(SIMPLE_FB_MSG_ACTION)
            elif action == CUSTOM_EVENT_ID:
                print(CUSTOM_EVENT_ID)
                request = get_custom_event_post_example(
                    sender_id=sender_id,
                    event_id=event_id
                )
                self.custom_evt_agent.process_request(request)
            else:
                print(BLANK_ACTION)
