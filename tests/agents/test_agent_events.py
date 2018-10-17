import unittest
from mock import patch

from chatbot.integrations.eventbrite import EventbriteIntegration
from chatbot.agents.builder import (
    build_agent_by_intent_diplayname,
    EVENT_AGENT,
)
from chatbot.integrations.builder import (
    EB_INTEGRATION,
    build_integration_by_source,
)


class TestAgentEvent(unittest.TestCase):
    """docstring for TestAgentBase"""

    def setUp(self):
        super(TestAgentEvent, self).setUp()
        self.event_agent = EVENT_AGENT
        self.event_integration = build_integration_by_source(EB_INTEGRATION)
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
        get_params = self.event_integration.map_get_params({'geo-city': 'San Francisco'})
        with patch.object(EventbriteIntegration, 'respond', return_value=None) as mock_method:
            agent_built.process_request(self.post)
            mock_method.assert_called_once_with(
                endpoint=self.event_integration.EB_EVENTS_ENDPOINT_BY_ORG,
                limit=3,
                params=get_params,
                target='events'
            )
