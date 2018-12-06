from chatbot.agents.base import Agent
from chatbot.integrations.builder import (
    FB_INTEGRATION,
    build_integration_by_source,
)
from chatbot.utils import (
    get_logger,
    LOG_AGENT_DIR,
)


class LiveChatAgent(Agent):
    """Agent that processes events"""
    def __init__(self):
        super(LiveChatAgent, self).__init__()
        self.logger = get_logger('livechat_agent', LOG_AGENT_DIR)
        self.messenger_integration = build_integration_by_source(FB_INTEGRATION)

    def process_request(self, post):
        self.logger.info(post)
        intent = post.get('originalDetectIntentRequest')
        if (
            intent.get('payload') and
            intent.get('source') == FB_INTEGRATION
        ):
            # get sender_id for respond
            sender_id = self.messenger_integration.get_sender_id(post)
            # Send pass thread with Haandover protocol
            self.messenger_integration.send_pass_thread(sender_id)
