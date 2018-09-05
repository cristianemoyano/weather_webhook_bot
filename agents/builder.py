from agents.events import EventAgent
from agents.forecast import ForecastAgent
from agents.exceptions import UndefinedAgent


AGENT_BY_NAME = {
    'Event': EventAgent,
    'CheckWeather': ForecastAgent,
}


def build_agent_by_intent_diplayname(name):
    """Get a tax declaration manager class depending on the given currency and instantiate the object."""
    agent = AGENT_BY_NAME.get(name, None)
    if agent:
        return agent()
    else:
        raise UndefinedAgent(name)
