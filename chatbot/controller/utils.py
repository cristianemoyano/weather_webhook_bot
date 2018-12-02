from chatbot.routes import APP_ROUTES


def get_route(view):
    return APP_ROUTES.get(view).get('route')


def get_methods(view):
    return APP_ROUTES.get(view).get('methods')


def get_intent_display_name(post):
    intent_display_name = None
    try:
        intent_display_name = post.get('queryResult').get('intent').get('displayName')
    except AttributeError:
        intent_display_name = None

    try:
        intent_display_name = intent_display_name or post.get('result').get('action')
    except AttributeError:
        intent_display_name = None

    return intent_display_name
