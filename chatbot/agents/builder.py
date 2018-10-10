from chatbot.agents.events import EventAgent
from chatbot.agents.forecast import ForecastAgent
from chatbot.agents.exceptions import UndefinedAgent

EVENT_AGENT = 'events.search'
FORECAST_AGENT = 'CheckWeather'

AGENT_BY_NAME = {
    EVENT_AGENT: EventAgent,
    FORECAST_AGENT: ForecastAgent,
}


def build_agent_by_intent_diplayname(name):
    """Get a tax declaration manager class depending on the given currency and instantiate the object."""
    agent = AGENT_BY_NAME.get(name, None)
    if agent:
        return agent()
    else:
        raise UndefinedAgent(name)
