import os
from setuptools import setup
from setuptools import find_packages
from setuptools.command.install import install


class CustomInstall(install):
    def run(self):
        install.run(self)
        from nxtodo import initialize
        initialize("nxtodo_cli", "nxtodo_cli",
                   "nxtodo_cli", "nxtodo_cli.settings")


setup(
    name='nxtodo_cli',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'nxtodo==1.0',
        'colored==1.3.5',
        'prettytable==0.7.2'
    ],
    entry_points={
        'console_scripts': [
            'nxtodo=nxtodo_cli.main:main'
        ]
    },
    package_data={
        'nxtodo_cli': ['default.ini']
    },
    data_files=[
        (os.path.join(os.environ['HOME'], '.nxtodo'),
         [os.path.join(os.path.dirname(__file__), 'config.ini')])
    ],
    license='MIT',
    author='kharivitalij',
    author_email='nikita.kharitonov99@gmail.com',
    cmdclass={
        'install': CustomInstall,
    },
    description='Console client for nxtodo library.'
)
