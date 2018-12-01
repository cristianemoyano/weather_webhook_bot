from chatbot.agents.base import Agent
from chatbot.integrations.builder import (
    FB_INTEGRATION,
    build_integration_by_source,
)


class LiveChatAgent(Agent):
    """Agent that processes events"""
    def __init__(self):
        super(LiveChatAgent, self).__init__()

    def process_request(self, post):
        print(post)
        intent = post.get('originalDetectIntentRequest')
        if (
            intent.get('payload') and
            intent.get('source') == FB_INTEGRATION
        ):
            # Build FB integration
            integration = build_integration_by_source(intent.get('source'))
            # get sender_id for respond
            sender_id = post.get('originalDetectIntentRequest').get('payload').get('data').get('sender').get('id')
            integration.send_pass_thread(sender_id)
