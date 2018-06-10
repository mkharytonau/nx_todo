import logging
from nxtodo.thirdparty import CompletionError


def log_add_query(success, error):
    logger = logging.getLogger('nxtodo_logger')
    def log_add(func):
        def wrapper(*args, **kwargs):
            try:
                entity_id = func(*args, **kwargs)
                #logger.info(success.format(args[1], args[0]))
                logger.info(success + str(args) + str(kwargs))
                return entity_id
            except Exception as e:
                #logger.error(error.format(args[1]) + str(e))
                logger.error(error)
        return wrapper
    return log_add


def log_complete_query(success, error):
    def log_complete(func):
        def wrapper(user_name, entity_id):
            try:
                func(user_name, entity_id)
                logging.info(success.format(entity_id))
            except PermissionError as e:
                logging.error(error.format(entity_id) + str(e))
                raise PermissionError(str(e)) # only raise
            except CompletionError as e:
                logging.error(error.format(entity_id) + str(e))
                raise CompletionError(str(e))
        return wrapper
    return log_complete