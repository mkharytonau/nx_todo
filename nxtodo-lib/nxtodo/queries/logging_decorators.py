import logging
from functools import wraps

from nxtodo.common.constants import LOGGER_NAME
from nxtodo.common.exceptions import (
    CompletionError,
    ObjectDoesNotFound,
    Looping
)


def log_user_query(success, error):
    """Logs functions, that manage users.

    :param success: success message
    :param error: error message

    """

    logger = logging.getLogger(LOGGER_NAME)

    def log(func):
        @wraps(func)
        def wrapper(user_name):
            try:
                result = func(user_name)
                logger.info(success.format(user_name))
                return result
            except Exception as e:
                logger.error(error.format(user_name) + str(e))
                raise

        return wrapper

    return log


def log_get_query(success, error):
    """Logs get query.

    :param success: success message
    :param error: error message

    """

    logger = logging.getLogger(LOGGER_NAME)

    def log(func):
        @wraps(func)
        def wrapper(user_name, *args, **kwargs):
            try:
                result = func(user_name, *args, **kwargs)
                logger.info(success.format(len(result), user_name))
                return result
            except ObjectDoesNotFound as e:
                logger.error(error.format(user_name) + str(e))
                raise
            except Exception as e:
                logger.error(error.format(user_name) + str(e))
                raise
        return wrapper
    return log


def log_add_query(success, error):
    """Logs add query.

    :param success: success message
    :param error: error message

    """

    logger = logging.getLogger(LOGGER_NAME)

    def log(func):
        @wraps(func)
        def wrapper(user_name, *args, **kwargs):
            try:
                entity_id = func(user_name, *args, **kwargs)
                logger.info(success.format(entity_id, user_name))
                return entity_id
            except ObjectDoesNotFound as e:
                logger.error(error.format(user_name) + str(e))
                raise
            except Looping as e:
                logger.error(error.format(user_name) + str(e))
                raise
            except Exception as e:
                logger.error(error.format(user_name) + str(e))
                raise
        return wrapper
    return log


def log_edit_query(success, error):
    """Logs edit query.

    :param success: success message
    :param error: error message

    """

    logger = logging.getLogger(LOGGER_NAME)

    def log(func):
        @wraps(func)
        def wrapper(user_name, entity_id, *args, **kwargs):
            try:
                func(user_name, entity_id, *args, **kwargs)
                logger.info(success.format(entity_id, user_name))
            except ObjectDoesNotFound as e:
                logger.error(error.format(entity_id, user_name) + str(e))
                raise
            except PermissionError as e:
                logger.error(error.format(entity_id, user_name) + str(e))
                raise
            except Exception as e:
                logger.error(error.format(entity_id, user_name) + str(e))
                raise
        return wrapper
    return log


def log_addto_query(success, error):
    """Logs addto query.

    :param success: success message
    :param error: error message

    """

    logger = logging.getLogger(LOGGER_NAME)

    def log(func):
        @wraps(func)
        def wrapper(user_name, to_entity, entities):
            try:
                func(user_name, to_entity, entities)
                msg = success.format(entities, to_entity, user_name)
                logger.info(msg)
            except ObjectDoesNotFound as e:
                msg = error.format(entities, to_entity, user_name) + str(e)
                logger.error(msg)
                raise
            except PermissionError as e:
                msg = error.format(entities, to_entity, user_name) + str(e)
                logger.error(msg)
                raise
            except Looping as e:
                msg = error.format(entities, to_entity, user_name) + str(e)
                logger.error(msg)
                raise
            except Exception as e:
                msg = error.format(entities, to_entity, user_name) + str(e)
                logger.error(msg)
                raise
        return wrapper
    return log


def log_query(success, error):
    """Logs common queries, like complete or remove.

    :param success: success message
    :param error: error message

    """

    logger = logging.getLogger(LOGGER_NAME)

    def log(func):
        @wraps(func)
        def wrapper(user_name, entity_id):
            try:
                func(user_name, entity_id)
                logger.info(success.format(entity_id, user_name))
            except ObjectDoesNotFound as e:
                logger.error(error.format(entity_id, user_name) + str(e))
                raise
            except PermissionError as e:
                logger.error(error.format(entity_id, user_name) + str(e))
                raise
            except CompletionError as e:
                logger.error(error.format(entity_id, user_name) + str(e))
                raise
            except Exception as e:
                logger.error(error.format(entity_id, user_name) + str(e))
                raise
        return wrapper
    return log


