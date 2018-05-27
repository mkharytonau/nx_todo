import os, sys
from setuptools import setup
from setuptools.command.install import install


class CustomInstallCommand(install):
    def run(self):
        if os.system('which psql'):
            str = 'not installed'
        else:
            str = 'installed'
        os.system("notify-send '" + str + "'")
        #print("Hello, developer, how are you? :)")
        #os.system("sudo -u postgres psql -c \"create user nxtodo_install password 'todoinstall'\"")
        #os.system("sudo -u postgres psql -c 'create database nxtodo_test_install owner nxtodo_install'")
        #install.run(self)

        #sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        #os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nxtodo.settings")
        #from django.core.management import execute_from_command_line
        #execute_from_command_line(['manage.py', 'makemigrations'])
        #execute_from_command_line(['manage.py', 'migrate'])

        #print('Finished')


setup(
    name='nxtodo',
    version='1.0',
    packages=['nxtodo',
    'nxtodo.daemon',
    'nxtodo.database',
    'nxtodo.nxtodo_db',
    'nxtodo.nxtodo_db.migrations',
    'nxtodo.reminding',
    'nxtodo.thirdparty'],
    url='',
    license='',
    author='kharivitalij',
    author_email='',
    cmdclass={
        'install': CustomInstallCommand,
    },
    #install_requires=[
    #    'notify2',
    #    'psycopg2',
    #    'django==1.11'
    #]
)
