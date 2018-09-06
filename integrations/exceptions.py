class UndefinedIntegration(Exception):
    """Raised when attempting to get a non defined integration."""

    def __init__(self, param):
        super(Exception, self).__init__('Undefined Integration for: {param}'.format(param=param))


class UndefinedElementType(Exception):
    """Raised when attempting to get a non defined ElementType."""

    def __init__(self, param):
        super(Exception, self).__init__('Undefined ElementType for: {param}'.format(param=param))
