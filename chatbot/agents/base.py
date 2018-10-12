class Agent(object):
    def __init__(self, request_url=None):
        self.request_url = request_url

    def process_request(self):
        raise NotImplementedError()
