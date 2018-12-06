import logging
from chatbot.constants import IS_LOG_FILE_HANDLER_ACTIVE

LOG_AGENT_DIR = 'chatbot/logs/agents/'


def get_logger(agent, path, file_handler_active=True, stream_handler_active=True):
    # create logger
    logger = logging.getLogger(agent)
    logger.setLevel(logging.DEBUG)

    # create handlers and set level to debug
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(
        filename='{path}{agent}.log'.format(path=path, agent=agent)
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
