import configparser


def get_config():
    config = configparser.ConfigParser()
    try:
        config_path = '/home/kharivitalij/nxtodo-project/config.ini'
        config.read(config_path)
        if not config.sections():
            raise FileNotFoundError
    except FileNotFoundError:
        config_path = 'default.ini'
        config.read(config_path)
    return config


def identify_user(args, config):
    try:
        return args.user if args.user is not None else config['user']['name']
    except KeyError:
        raise KeyError('Error during user definition, please, '
                       'check your config file.')