from dateutil import parser

from chatbot.agents.base import Agent
from chatbot.integrations.builder import build_integration_by_source


class ForecastAgent(Agent):
    """Agent that processes forecast"""
    def __init__(self):
        super(ForecastAgent, self).__init__()
        self.forecast_integration = 'openweathermap'

    def process_request(self, post):
        print(post)
        if post.get('queryResult').get('intent').get('displayName') != "CheckWeather":
            return {}

        result = post.get("queryResult")
        parameters = result.get("parameters")
        city = parameters.get("geo-city")
        querydate = parameters.get("date")
        try:
            parsed_date = parser.parse(querydate)
            date = parsed_date.strftime("%Y-%m-%d")
        except Exception:
            date = ''

        if city is None:
            return None
        forecast_integration = build_integration_by_source(self.forecast_integration)
        r = forecast_integration.respond(city)
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
