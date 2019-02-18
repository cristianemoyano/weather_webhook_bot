import requests

from ..integrations.base import Integration
from ..constants import (
    SLACK_WEBHOOK,
)


class SlackIntegration(Integration):
    """docstring for SlackIntegration"""
    def __init__(self):
        super(SlackIntegration, self).__init__()

    def send_message(self, message):
        data = {
            "text": str(message)
        }
        headers = {
            "content-type": "application/json"
        }
        return requests.post(
            SLACK_WEBHOOK,
            json=data,
            headers=headers
        )
