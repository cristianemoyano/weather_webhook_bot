# chatbot
[![Build Status](https://travis-ci.org/cristianemoyano/weather_webhook_bot.svg?branch=master)](https://travis-ci.org/cristianemoyano/weather_webhook_bot)

[![Coverage Status](https://coveralls.io/repos/github/cristianemoyano/weather_webhook_bot/badge.svg)](https://coveralls.io/github/cristianemoyano/weather_webhook_bot)

App that communicates with the apiV2 of a bot in [DialogFlow](https://dialogflow.com/)


## Environment

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

## Running Locally

```sh
$ pip install -r requirements.txt
$ git clone https://github.com/cristianemoyano/weather_webhook_bot.git # or clone your own fork
$ python server.py
```

Your app should now be running on [localhost:5000](http://localhost:5000/).

## Testing

#### Doc
[Pytest Doc](https://docs.pytest.org/en/latest/)

#### Run suite
```
$ python test_suite.py test
```

#### Run specific test cases
```
$ pytest tests/<folder>/test_xxxx.py::TestClass
```

#### Debugging
```
import ipdb;ipdb.set_trace()
```
turn off capture output:
```
$ pytest -s test_case_01.py
```

## Heroku

#### deploying to Heroku in a new app

Make sure you have [Heroku CLI](https://cli.heroku.com/) installed.

```
$ heroku create <name>
$ git push heroku master
$ heroku open
```

##### View heroku logs
`heroku logs`

##### deploy a new version
You must have the correct credentials
```sh
$ git push heroku master
```

##### heroku app
[Heroku app](https://weather-webhook-bot-app.herokuapp.com/)


## New git release
[Git Basics - Tagging](https://git-scm.com/book/en/v2/Git-Basics-Tagging)
```sh
$ gco master
$ git pull origin master
$ git tag -a v1.4 -m "my version 1.4"
$ git push origin v1.4
```
