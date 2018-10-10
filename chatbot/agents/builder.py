from chatbot.agents.events import EventAgent
from chatbot.agents.forecast import ForecastAgent
from chatbot.agents.exceptions import UndefinedAgent


AGENT_BY_NAME = {
    'events.search': EventAgent,
    'CheckWeather': ForecastAgent,
}


def build_agent_by_intent_diplayname(name):
    """Get a tax declaration manager class depending on the given currency and instantiate the object."""
    agent = AGENT_BY_NAME.get(name, None)
    if agent:
        return agent()
    else:
        raise UndefinedAgent(name)
