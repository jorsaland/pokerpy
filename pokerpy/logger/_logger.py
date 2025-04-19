"""
Defines the function that calls the PokerPy logger.
"""


import logging


from pokerpy.constants import LOGGER_FORMAT, LOGGER_NAME


def get_logger():

    """
    Calls the PokerPy logger.
    """

    logger = logging.getLogger(LOGGER_NAME)

    if not logger.hasHandlers():

        formatter = logging.Formatter(LOGGER_FORMAT)
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)

        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)
    
    return logger