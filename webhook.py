import json
import os
import requests

from flask import Flask
from flask import request
from flask import make_response
from dateutil import parser

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print(json.dumps(req, indent=4))

    res = makeResponse(req)
    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def makeResponse(req):
    print(req)
    if req.get('queryResult').get('intent').get('displayName') != "CheckWeather":
        return {}

    result = req.get("queryResult")
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


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=True, port=port, host='0.0.0.0')
