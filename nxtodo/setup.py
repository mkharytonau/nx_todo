import os, sys
from setuptools import setup
from setuptools.command.install import install


class CustomInstallCommand(install):
    def run(self):
        #os.system(
        #    "sudo -u postgres psql -c \"create user nxtodo_install password 'todoinstall'\"")
        #os.system(
        #    "sudo -u postgres psql -c 'create database nxtodo_test_install owner nxtodo_install'")
        install.run(self)
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from nxtodo import initialize
        initialize()

setup(
    name='nxtodo',
    version='1.0',
    packages=['nxtodo',
              'nxtodo.configuration',
              'nxtodo.nxtodo_db',
              'nxtodo.nxtodo_db.migrations',
              'nxtodo.queries',
              'nxtodo.reminding',
              'nxtodo.thirdparty'],
    url='',
    license='',
    author='kharivitalij',
    author_email='',
    cmdclass={
        'install': CustomInstallCommand,
    },
    install_requires=[
        'psycopg2-binary==2.7.4',
        'django==1.11'
    ]
)
