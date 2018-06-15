import os
import configparser
from nxtodo.thirdparty import LogLevels


def get_config():
    config = configparser.ConfigParser()
    try:
        config_path = os.path.join(os.environ['HOME'], '.nxtodo', 'config.ini')
        config.read(config_path)
        if not config.sections():
            raise FileNotFoundError
    except FileNotFoundError:
        packdir = os.path.split(os.path.dirname(__file__))[0]
        config_path = os.path.join(packdir, 'default.ini')
        config.read(config_path)
    config['logger']['logs_dir'] = logs_path(config['logger']['logs_dir'])
    config['logger']['logs_level'] = logs_level(config['logger']['logs_level'])
    return config


def logs_level(string):
    return str(getattr(LogLevels, string, LogLevels.DISABLED).value)


def logs_path(string):
    if string == 'cwd':
        string = os.getcwd()
    return os.path.join(string, 'nxtodo.log')


def identify_user(args, config):
    try:
        if args.entity == 'user':
            return None
        return args.user if args.user else config['user']['name']
    except KeyError:
        raise KeyError('Error during user definition, please, '
                       'check your config file.')