import logging


def get_common_logger() -> logging:
    """
    get the common logger and return
    :return:
    """
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    return logging.getLogger(__name__)
