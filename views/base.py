from constants import ROOT_PATH


class View(object):
    """HTML views"""
    def __init__(self):
        super(View, self).__init__()
        self.template_name = 'undefined'

    def render(self):
        raise NotImplementedError()

    def get_template_path(self, extension='.html'):
        return ROOT_PATH + '/templates/' + self.template_name + extension
