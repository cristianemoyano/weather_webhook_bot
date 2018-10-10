import unittest
import pytest

from chatbot.agents.events import EventAgent
from chatbot.agents.builder import (
    build_agent_by_intent_diplayname,
    EVENT_AGENT
)
from chatbot.agents.exceptions import UndefinedAgent


class TestAgentBuilder(unittest.TestCase):
    """docstring for TestAgentBase"""

    def setUp(self):
        super(TestAgentBuilder, self).setUp()
        self.agent_valid = EVENT_AGENT
        self.agent_wrong = 'wrong'

    def test_build_agent_by_intent_name_success(self):
        agent_built = build_agent_by_intent_diplayname(self.agent_valid)
        assert isinstance(agent_built, EventAgent)

    def test_build_agent_by_intent_name(self):
        with pytest.raises(UndefinedAgent):
            build_agent_by_intent_diplayname(self.agent_wrong)
