import unittest
from mock import patch

from ...app.integrations.openweathermap import OpenWeatherMapIntegration
from ...app.agents.builder import (
    build_agent_by_intent_diplayname,
    FORECAST_AGENT,
)


class MockClass(object):
    """docstring for MockClass"""
    def __init__(self, arg):
        super(MockClass, self).__init__()
        self.arg = arg

    def json(self):
        return self.arg


class TestAgentForecast(unittest.TestCase):
    """docstring for TestAgentBase"""

    def setUp(self):
        super(TestAgentForecast, self).setUp()
        self.forecast_agent = FORECAST_AGENT
        self.agent_wrong = 'wrong'
        self.post = {
            'queryResult': {
                'intent': {
                    'displayName': 'CheckWeather',
                },
                'parameters': {
                    'geo-city': 'San Francisco',
                    'date': '',
                },
            },
            'originalDetectIntentRequest': {
                'payload': 'data',
                'source': 'facebook',
            },
        }
        self.weather_response = {
            'list': [
                {
                    'dt_txt': '',
                    'weather': [
                        {
                            'description': ''
                        }
                    ],

                }
            ]
        }

    def test_event_agent_with_none_response(self):
        agent_built = build_agent_by_intent_diplayname(self.forecast_agent)
        mock_response = MockClass(self.weather_response)

        with patch.object(OpenWeatherMapIntegration, 'respond', return_value=mock_response) as mock_method:
            agent_built.process_request(self.post)
            mock_method.assert_called_once_with('San Francisco')
