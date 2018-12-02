from chatbot.agents.base import Agent
from chatbot.constants import DEBUG
from chatbot.agents.welcome import WelcomeAgent
from chatbot.integrations.sandbox import (
    get_facebook_welcome_payload,
    WELCOME_ACTION,
    SIMPLE_FB_MSG_ACTION,
    BLANK_ACTION
)


class SandBoxAgent(Agent):
    """Agent that processes events"""
    def __init__(self):
        super(SandBoxAgent, self).__init__()
        self.welcome_agent = WelcomeAgent()
        self.is_debug = DEBUG

    def process_request(self, post):
        if self.is_debug:
            print('-----------------SANDBOX------------------')
            print(post)
            print('-----------------SANDBOX------------------')
            action = post.get('action')
            if action == WELCOME_ACTION:
                request = get_facebook_welcome_payload(
                    sender_id=post.get('sender_id', '2093633150674633'),
                    recipient_id=post.get('recipient_id', '256171418366507')
                )
                print(request)
                self.welcome_agent.process_request(request)
            elif action == SIMPLE_FB_MSG_ACTION:
                print(SIMPLE_FB_MSG_ACTION)
            else:
                print(BLANK_ACTION)
