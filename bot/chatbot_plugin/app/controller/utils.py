def get_intent_display_name(post):
    intent_display_name = None
    try:
        intent_display_name = post.get('queryResult').get('intent').get('displayName')
        return intent_display_name
    except AttributeError:
        intent_display_name = None

    try:
        intent_display_name = intent_display_name or post.get('result').get('action')
        return intent_display_name
    except AttributeError:
        intent_display_name = None

    try:
        intent_display_name = intent_display_name or post.get('intent')
        return intent_display_name
    except AttributeError:
        intent_display_name = None
    return intent_display_name


def get_agent_name(post):
    agent_name = None
    try:
        agent_name = post.get('agent')
    except AttributeError:
        agent_name = None
    return agent_name


def get_lang_code(post):
    lang_code = None
    try:
        lang_code = post.get('queryResult').get('languageCode')
        return lang_code
    except AttributeError:
        lang_code = None
    try:
        lang_code = post.get('lang_code')
    except AttributeError:
        lang_code = None
        return lang_code
    return lang_code
