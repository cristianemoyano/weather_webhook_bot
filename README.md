# weather_webhook_bot
[![Build Status](https://travis-ci.org/cristianemoyano/weather_webhook_bot.svg?branch=master)](https://travis-ci.org/cristianemoyano/weather_webhook_bot)

[![Coverage Status](https://coveralls.io/repos/github/cristianemoyano/weather_webhook_bot/badge.svg)](https://coveralls.io/github/cristianemoyano/weather_webhook_bot)

App that communicates with the apiV2 of a bot in [DialogFlow](https://dialogflow.com/)


##### heroku app
[Heroku app](https://weather-webhook-bot-app.herokuapp.com/)


## Running Locally

Make sure you have [Heroku CLI](https://cli.heroku.com/) installed.

```sh
$ git clone https://github.com/cristianemoyano/weather_webhook_bot.git # or clone your own fork
$ python webhook.py
```

Your app should now be running on [localhost:5000](http://localhost:5000/).

## Deploying to Heroku in a new app

```
$ heroku create <name>
$ git push heroku master
$ heroku open
```

##### View heroku logs
`heroku logs`

##### deploy a new version
```sh
$ git push heroku master
```

> we recommend
```sh
$ cd ..
$ virtualenv env
$ source env/bin/activate
```

> set environment
```python
(env) $ export DEBUG=bool
(env) $ export EB_ACCESS_TOKEN=secret
```
