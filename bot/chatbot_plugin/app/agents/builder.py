from .events import (
    EventAgent,
    CustomEventAgent,
    GetEventByIdAgent,
    GetWebviewAgent,
)
from .welcome import WelcomeAgent
from .forecast import ForecastAgent
from .livechat import LiveChatAgent
from .exceptions import UndefinedAgent
from .sandbox import SandBoxAgent

CUSTOM_EVENT_AGENT = 'CustomEventSearch'
EVENT_AGENT = 'events.search'
FORECAST_AGENT = 'CheckWeather'
WELCOME_AGENT = 'DefaultWelcomeIntent'
LIVECHAT_AGENT = 'LiveChat'
SANDBOX_AGENT = 'SandBox'
GET_EVENT_BY_ID_AGENT = 'GetEventById'
GET_WEBVIEW_AGENT = 'get_webview'


AGENT_BY_NAME = {
    CUSTOM_EVENT_AGENT: CustomEventAgent,
    EVENT_AGENT: EventAgent,
    FORECAST_AGENT: ForecastAgent,
    WELCOME_AGENT: WelcomeAgent,
    LIVECHAT_AGENT: LiveChatAgent,
    SANDBOX_AGENT: SandBoxAgent,
    GET_EVENT_BY_ID_AGENT: GetEventByIdAgent,
    GET_WEBVIEW_AGENT: GetWebviewAgent,
}


def build_agent_by_intent_diplayname(name):
    """Get a tax declaration manager class depending on the given currency and instantiate the object."""
    agent = AGENT_BY_NAME.get(name, None)
    if agent:
        return agent()
    else:
        raise UndefinedAgent(name)
