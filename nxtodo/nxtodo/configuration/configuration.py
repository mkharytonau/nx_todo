import os, logging
from django.core.wsgi import get_wsgi_application
from nxtodo.thirdparty import LogLevels

# nxtodo.initialize('nxtodo', 'todotodo', 'nxtodo_test', 'nxtodo.configuration.settings_for_tests')


def initialize(psql_user="nxtodo", psql_password="todotodo",
               psql_db_name="nxtodo_db",
               settings_module="nxtodo.configuration.settings"):

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


def configure(settings_module="nxtodo.configuration.settings",
              log_file=os.path.join(os.path.dirname(__file__), 'nxtodo.log'),
              log_level=LogLevels.INFO.value):
    # Django configuration
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)
    get_wsgi_application()

    # Logger configuration
    logging.basicConfig(filename=log_file, level=log_level,
                        format='%(asctime)s %(message)s')
