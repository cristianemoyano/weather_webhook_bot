from integrations.facebook import FacebookIntegration
from integrations.exceptions import UndefinedIntegration


INTEGRATIONS_BY_NAME = {
    'facebook': FacebookIntegration,
}


def build_integration_by_source(name):
    """Get a tax declaration manager class depending on the given currency and instantiate the object."""
    integration = INTEGRATIONS_BY_NAME.get(name, None)
    if integration:
        return integration()
    else:
        raise UndefinedIntegration(name)
