import pytest
import unittest

from chatbot.agents.base import Agent


class TestAgentBase(unittest.TestCase):
    """docstring for TestAgentBase"""

    def setUp(self):
        super(TestAgentBase, self).setUp()
        self.agent = Agent()

    def test_not_implemented_error(self):
        with pytest.raises(NotImplementedError):
            self.agent.process_request()
