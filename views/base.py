class View(object):
    """HTML views"""
    def __init__(self):
        super(View, self).__init__()

    def render(self):
        raise NotImplementedError()
