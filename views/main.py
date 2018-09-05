from views.base import View


class IframeView(View):
    def __init__(self):
        super(IframeView, self).__init__()

    def render(self):
        msg = '<p>Try: Weather forecast in Mendoza today</p>'
        iframe = (
            '<iframe '
            'allow="microphone;"'
            'width="350"  '
            'height="430" '
            'src="https://console.dialogflow.com/api-client/demo/embedded/1a033c63-e5f9-4f42-b715-1db32e561b52">'
            '</iframe> '
        )
        return msg + iframe
