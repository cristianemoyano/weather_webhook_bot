import logging
import os
from chatbot.constants import (
    IS_LOG_FILE_HANDLER_ACTIVE,
)

# Logger
LOG_AGENT_DIR = 'chatbot/logs/agents/'


def get_logger(agent, path, file_handler_active=True, stream_handler_active=True):
    # create logger
    logger = logging.getLogger(agent)
    logger.setLevel(logging.DEBUG)

    # create handlers and set level to debug
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(
        filename=_get_log_path(
            log_dir=path,
            agent_name=agent,
        )
    )
    file_handler.setLevel(logging.INFO)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to handler
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    if IS_LOG_FILE_HANDLER_ACTIVE:
        logger.addHandler(file_handler)

    # add handler to logger
    logger.addHandler(console_handler)
    return logger


def _get_log_path(log_dir='chatbot/logs/', agent_name='undefined', extension='.log'):
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        return log_dir + agent_name + extension


PHRASES_TABLE = {
    'en': {
        'es': {
            'test': 'prueba',
            'Hey': 'Hola',
            'Hi !': 'Hola !',
            'I recommend these events!': 'te recomiendo éstos eventos!',
            'See event': 'Ver evento',
            'Tickets': 'Entradas',
            'Yes, more !': 'Si, más!',
            'more events': 'más eventos',
            'No, thanks!': 'No, gracias!',
            'thank you': 'Gracias!',
            'I found this event for you: ': 'Encontré éste evento para ti: ',
            'Sorry I have not found any event :(': 'Lo siento, no he encontrado ningún evento :(',
        }
    }
}


def translator(lang_in, lang_out, text_key):
    text = PHRASES_TABLE.get(lang_in).get(lang_out).get(text_key)
    if text:
        return text
    return text_key


def get_text(lang_out, text):
    # Translate a phrase from english to other language
    return translator('en', lang_out, text)
