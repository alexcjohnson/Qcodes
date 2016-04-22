import logging

# http://stackoverflow.com/questions/7621897/python-logging-module-globally

def setup_custom_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # if logger 'name' already exists, return it to avoid logging duplicate
    # messages by attaching multiple handlers of the same type
    if logger.handlers:
        return logger


    # formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
    # handler = logging.StreamHandler()
    # handler.setFormatter(formatter)

    # logger.addHandler(handler)
    return logger
