import os
from django.core.wsgi import get_wsgi_application


def initialize(psql_user="nxtodo", psql_password="todotodo",
               psql_db_name="nxtodo_db", settings_module="nxtodo.configuration.settings"):

    psql_cmd_create_user = "create user {} password '{}'".format(psql_user,
                                                                 psql_password)
    os.system("sudo -u postgres psql -c \"{}\"".format(psql_cmd_create_user))
    psql_cmd_create_db = "create database {} owner {}".format(psql_db_name,
                                                              psql_user)
    os.system("sudo -u postgres psql -c '{}'".format(psql_cmd_create_db))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'makemigrations'])
    execute_from_command_line(['manage.py', 'migrate'])


def configurate(settings_module="nxtodo.configuration.settings"):
    # Django configuration
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)
    get_wsgi_application()
