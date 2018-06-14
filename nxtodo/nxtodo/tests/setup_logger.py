import logging, nxtodo


def setup_logger(logs_path, logs_level, logs_format):
    logger = nxtodo.get_logger()
    handler = logging.FileHandler(logs_path)
    handler.setLevel(logs_level)
    formatter = logging.Formatter(logs_format)
    handler.setFormatter(formatter)
    logger.addHandler(handler)