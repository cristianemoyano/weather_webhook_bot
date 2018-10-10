from chatbot.views.base import View


class IframeView(View):
    def __init__(self):
        super(IframeView, self).__init__()
        self.template_name = 'iframe_view'

    def render(self):
        path_file = self.get_template_path()

        with open(path_file, 'r') as f:
            html = f.read()

        return html


class WebView(View):
    def __init__(self):
        super(WebView, self).__init__()
        self.template_name = 'webview'

    def render(self):
        path_file = self.get_template_path()

        with open(path_file, 'r') as f:
            html = f.read()

        return html
