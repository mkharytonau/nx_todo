import logging
from nxtodo.thirdparty import CompletionError


def log_add_queri(success, error):
    def log_add(func):
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
                logging.info(success.format(args[1], args[0]))
            except Exception as e:
                logging.error(error.format(args[1]) + str(e))
        return wrapper
    return log_add


def log_complete_queri(success, error):
    def log_complete(func):
        def wrapper(user_name, entity_id):
            try:
                func(user_name, entity_id)
                logging.info(success.format(entity_id))
            except PermissionError as e:
                logging.error(error.format(entity_id) + str(e))
                raise PermissionError(str(e))
            except CompletionError as e:
                logging.error(error.format(entity_id) + str(e))
                raise CompletionError(str(e))
        return wrapper
    return log_complete