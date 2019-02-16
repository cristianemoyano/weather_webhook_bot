class Agent(object):
    def __init__(self, request_url=None, lang_code='en'):
        self.request_url = request_url
        self.lang_code = lang_code
        self.required_params = []

    def process_request(self):
        raise NotImplementedError()
