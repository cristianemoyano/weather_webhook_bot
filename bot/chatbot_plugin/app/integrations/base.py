class Integration(object):
    """Parent class for Integrations"""
    def __init__(self):
        super(Integration, self).__init__()

    def respond(self):
        raise NotImplementedError()
