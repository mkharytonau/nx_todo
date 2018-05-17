import getpass
import os
from setuptools import setup
from setuptools import find_packages


setup(
    name='nxtodo',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'colored',
        'notify2'
    ],
    entry_points={
        'console_scripts': [
            'nxtodo=nxtodo.main:main'
        ]
    },
    package_data={
        'nxtodo.nxtodo_lib': [
            'img/icon.png',
            'database/db.json'
        ]
    },
    data_files=[
        (os.path.join('/','home', getpass.getuser(), '.nxtodo','config'), ['config/config.ini'])
    ],
    license='MIT',
    author='kharivitalij',
    author_email='nikita.kharitonov99@gmail.com',
    description='first setup'
)
