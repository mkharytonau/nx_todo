from setuptools import setup
from setuptools import find_packages

setup(
    name='nxtodo',
    version='1.0',
    packages=find_packages(exclude=['nxtodo.nxtodo_web']),
    url='',
    license='MIT',
    author='kharivitalij',
    author_email='nikita.kharitonov99@gmail.com',
    description='first setup'
)
