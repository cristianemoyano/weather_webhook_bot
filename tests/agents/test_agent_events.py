import unittest
from mock import patch

from chatbot.integrations.eventbrite import EventbriteIntegration
from chatbot.agents.builder import (
    build_agent_by_intent_diplayname,
    EVENT_AGENT,
)


class TestAgentEvent(unittest.TestCase):
    """docstring for TestAgentBase"""

    def setUp(self):
        super(TestAgentEvent, self).setUp()
        self.event_agent = EVENT_AGENT
        self.agent_wrong = 'wrong'
        self.post = {
            'queryResult': {
                'parameters': {
                    'geo-city': 'San Francisco',
                },
            },
            'originalDetectIntentRequest': {
                'payload': 'data',
                'source': 'facebook',
            },
        }

    def test_event_agent_with_none_response(self):
        agent_built = build_agent_by_intent_diplayname(self.event_agent)
        with patch.object(EventbriteIntegration, 'respond', return_value=None) as mock_method:
            agent_built.process_request(self.post)
            mock_method.assert_called_once_with(
                endpoint='/events/search/',
                limit=3,
                params={'location.address': 'San Francisco'},
                target='events'
            )
