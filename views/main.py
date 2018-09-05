from views.base import View


class IframeView(View):
    def __init__(self):
        super(IframeView, self).__init__()

    def render(self):
        msg = '<p>Try: find me 2 tickets to Madonnas concert in New York</p>'
        iframe = (
            '<iframe '
            'allow="microphone;"'
            'width="350"  '
            'height="430" '
            'src="https://console.dialogflow.com/api-client/demo/embedded/59b4f5f8-6110-45dd-b110-82e42bc3bb47">'
            '</iframe> '
        )
        return msg + iframe
