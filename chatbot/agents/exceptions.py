class UndefinedAgent(Exception):
    """Raised when attempting to get a non defined agent."""

    def __init__(self, param):
        super(Exception, self).__init__('Undefined Agent for: {param}'.format(param=param))
