import requests

from .base import Integration
from ..constants import OPENWEATHERMAP_KEY


class OpenWeatherMapIntegration(Integration):
    """docstring for EventbriteIntegration"""
    def __init__(self):
        super(OpenWeatherMapIntegration, self).__init__()
        self.url = 'http://api.openweathermap.org/data/2.5/forecast?q='

    def respond(self, city):
        return requests.get(
            self.url + city + '&appid=' + OPENWEATHERMAP_KEY
        )
