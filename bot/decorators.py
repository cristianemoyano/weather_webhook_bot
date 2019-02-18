from functools import wraps
from time import time
from .utils import get_datetime_in_utc
from .chatbot_plugin.app.integrations.slack import SlackIntegration


def timing_and_reporting(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time()
        result = f(*args, **kwargs)
        end = time()
        request = args[1]
        elapsed_time = end - start
        query_params = request.query_params
        params = {}
        for key in query_params.keys():
            if key != "token":
                params.update(
                    {key: query_params.get(key)}
                )
        message = 'user_id {id} - user: {user} - datetime_utc: {utc} - elapsed_seconds: {s} - params: {params}'.format(
            id=request.user.pk,
            user=request.user.username,
            utc=get_datetime_in_utc(),
            s=elapsed_time,
            params=params
        )
        response = ' - request_code: {code} - data: {data}'.format(
            code=result.status_code,
            data=result.data.__str__()
        )
        message += response
        print(message)
        slack_client = SlackIntegration()
        response = slack_client.send_message(
            message=message
        )
        print(response)
        return result
    return wrapper
