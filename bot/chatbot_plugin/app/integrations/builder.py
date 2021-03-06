from .facebook import FacebookIntegration
from .eventbrite import EventbriteIntegration
from .openweathermap import OpenWeatherMapIntegration
from .exceptions import UndefinedIntegration

FB_INTEGRATION = 'facebook'
EB_INTEGRATION = 'eventbrite'
OPEN_WEATHER_MAP = 'openweathermap'

INTEGRATIONS_BY_NAME = {
    FB_INTEGRATION: FacebookIntegration,
    EB_INTEGRATION: EventbriteIntegration,
    OPEN_WEATHER_MAP: OpenWeatherMapIntegration,
}


def build_integration_by_source(name):
    """Get a tax declaration manager class depending on the given currency and instantiate the object."""
    integration = INTEGRATIONS_BY_NAME.get(name, None)
    if integration:
        return integration()
    else:
        raise UndefinedIntegration(name)
