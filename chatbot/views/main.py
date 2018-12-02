from chatbot.views.base import View
from flask import render_template
from chatbot.integrations.sandbox import (
    CONTEXT_ACTIONS,
)


class IframeView(View):
    def __init__(self):
        super(IframeView, self).__init__()
        self.template_name = 'iframe_view'

    def render(self):
        template = self.get_template()
        return render_template(template)


class WebView(View):
    def __init__(self):
        super(WebView, self).__init__()
        self.template_name = 'webview'

    def render(self):
        template = self.get_template()
        return render_template(template)


class SandboxView(View):
    def __init__(self):
        super(SandboxView, self).__init__()
        self.template_name = 'sandbox'

    def render(self):
        template = self.get_template()
        context = {
            'actions': CONTEXT_ACTIONS
        }
        return render_template(
            template,
            **context
        )
