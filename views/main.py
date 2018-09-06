from views.base import View
from constants import ROOT_PATH


class IframeView(View):
    def __init__(self):
        super(IframeView, self).__init__()

    def render(self):
        path_file = ROOT_PATH + '/templates/iframe_view.html'

        with open(path_file, 'r') as f:
            html = f.read()

        return html
