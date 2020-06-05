from setuptools import setup
from setuptools import find_packages

DESCRIPTION = """nxtodo - is a library that will allow you to create users, '
                'tasks, events, plans, reminders, store them in the database '
                'and manage them as you want."""

setup(
    name='nxtodo',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'psycopg2-binary==2.7.4',
        'django==1.11.29'
    ],
    license='MIT',
    author='kharivitalij',
    author_email='nikita.kharitonov99@gmail.com',
    description=DESCRIPTION
)
