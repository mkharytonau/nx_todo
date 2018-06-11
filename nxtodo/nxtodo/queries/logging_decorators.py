import logging
from nxtodo.thirdparty.exceptions import (
    CompletionError,
    ObjectDoesNotFound,
    NoNotifications,
    Looping
)


def log_query(success, error):
    logger = logging.getLogger('nxtodo_logger')

    def log(func):
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                logger.info(success + str(args) + str(kwargs))
                return result
            except ObjectDoesNotFound as e:
                logger.error(error + str(e))
                raise
            except PermissionError as e:
                logger.error(error + str(e))
                raise
            except CompletionError as e:
                logger.error(error + str(e))
                raise
            except Looping as e:
                logger.error(error + str(e))
                raise
            except NoNotifications as e:
                logger.error(error + str(e))
                raise
            except Exception as e:
                logger.error(error + str(e))
                raise
        return wrapper
    return log
