def identify_user(args, config):
    try:
        return args.user if args.user is not None else config['user']['name']
    except KeyError:
        raise KeyError('Error during user definition, please, check your config file.')