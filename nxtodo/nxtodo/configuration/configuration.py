import os, logging
from django.core.wsgi import get_wsgi_application
from nxtodo.thirdparty.common_data import LOGGER_NAME


CREATE_USER = "create user {} password '{}'"
CREATE_DATEBASE = "create database {} owner {}"


def initialize(
        psql_user="nxtodo",
        psql_password="todotodo",
        psql_db_name="nxtodo",
        settings_module="nxtodo.configuration.settings"):

    psql_cmd_create_user = CREATE_USER.format(psql_user, psql_password)
    os.system("sudo -u postgres psql -c \"{}\"".format(psql_cmd_create_user))
    psql_cmd_create_db = CREATE_DATEBASE.format(psql_db_name, psql_user)
    os.system("sudo -u postgres psql -c '{}'".format(psql_cmd_create_db))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'makemigrations'])
    execute_from_command_line(['manage.py', 'migrate'])


def configure(settings_module="nxtodo.configuration.settings"):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)
    get_wsgi_application()


def get_logger():
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.DEBUG)
    return logger
