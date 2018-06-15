from nxtodo import queries
from nxtodo.thirdparty.exceptions import ObjectDoesNotFound
from nxtodo_cli.view import show_user_table


USER_CHOICE_USER = {
    'add': lambda args, config: add_user(args),
    'remove': lambda args, config: remove_user(args),
    'show': lambda args, config: show_user(args, config),
}


def handle_user(args, config):
    USER_CHOICE_USER.get(args.command)(args, config)


def add_user(args):
    user_name = queries.add_user(args.name)
    print(user_name)


def remove_user(args):
    try:
        queries.remove_user(args.name)
    except ObjectDoesNotFound as e:
        print(e)


def show_user(args, config):
    try:
        users = queries.get_users(args.name)
    except ObjectDoesNotFound as e:
        print(e)
        return

    show_user_table(users, config)