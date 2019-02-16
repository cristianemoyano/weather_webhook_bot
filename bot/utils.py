from bot.chatbot_plugin.app.controller.utils import (
    get_intent_display_name,
    get_agent_name,
    get_lang_code,
)


def get_required_params(post, url):
    intent_display_name = get_intent_display_name(post)
    agent_name = get_agent_name(post)
    agent_name_defined = intent_display_name or agent_name
    lang_code = get_lang_code(post)
    return {
        'agent_name': agent_name_defined,
        'url': url,
        'lang_code': lang_code,
        'params': post,
    }
