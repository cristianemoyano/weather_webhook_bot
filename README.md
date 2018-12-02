# chatbot
[![Build Status](https://travis-ci.org/cristianemoyano/weather_webhook_bot.svg?branch=master)](https://travis-ci.org/cristianemoyano/weather_webhook_bot)

[![Coverage Status](https://coveralls.io/repos/github/cristianemoyano/weather_webhook_bot/badge.svg?branch=master)](https://coveralls.io/github/cristianemoyano/weather_webhook_bot?branch=master)

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
(env) $ export EB_ACCESS_TOKEN=str
(env) $ EB_IS_BY_ORGANIZATION=bool
(env) $ EB_ORGANIZATION_ID=int
(env) $ FB_INBOX_APP_ID=int
(env) $ FB_MESSENGER_ACCESS_TOKEN=str
(env) $ OPENWEATHERMAP_KEY=int
```

> or create .env in code/chatbot/.env:
```
DEBUG=1
EB_ACCESS_TOKEN=23
EB_IS_BY_ORGANIZATION=1
EB_ORGANIZATION_ID=61565826027
FB_INBOX_APP_ID=1
FB_MESSENGER_ACCESS_TOKEN=234
OPENWEATHERMAP_KEY=345
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

## Makefile

For new releases:
```sh
$ make new_release:
```

To deploy on Heroku:
```sh
$ make deploy
```

Run all test:
```sh
$ make test
```

Run app:
```
$ make run
```

To install dependencies:
```sh
$ make setup
```

To clean git local branches
```sh
$ make clean_local_branches
```

To see Heroku logs:
```sh
$ make logs
```
