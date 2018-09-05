import requests

from base import Agent
from dateutil import parser


class ForecastAgent(Agent):
    """Agent that processes events"""
    def __init__(self):
        super(ForecastAgent, self).__init__()

    def process(self, post):
        print(post)
        if post.get('queryResult').get('intent').get('displayName') != "CheckWeather":
            return {}

        result = post.get("queryResult")
        parameters = result.get("parameters")
        city = parameters.get("geo-city")
        querydate = parameters.get("date")
        parsed_date = parser.parse(querydate)
        date = parsed_date.strftime("%Y-%m-%d")
        if city is None:
            return None
        r = requests.get(
            'http://api.openweathermap.org/data/2.5/forecast?q=' + city + '&appid=06f070197b1f60e55231f8c46658d077'
        )
        json_object = r.json()
        weather = json_object['list']
        condition = ''
        for i in range(0, 30):
            if date in weather[i]['dt_txt']:
                condition = str(weather[i]['weather'][0]['description'])
                break
        speech = "The forecast for " + city + " at " + date + " is " + condition
        return {
            "fulfillmentText": speech,
            "source": "weather-webhook-bot-app.herokuapp.com/webhook",
        }
