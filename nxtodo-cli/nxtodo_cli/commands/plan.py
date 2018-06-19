from nxtodo import queries
from nxtodo.common import (
    Owner,
    AccessLevels
)
from nxtodo.common.exceptions import ObjectDoesNotFound
from nxtodo_cli.commands.common import with_printing_exception
from nxtodo_cli.displaying import show_plan_table

USER_CHOICE_PLAN = {
    'add': lambda user, args, config: add_plan(user, args),
    'show': lambda user, args, config: show_plan(user, args, config),
    'check': lambda user, args, config: check_plan(user, args),
    'edit': lambda user, args, config: edit_plan(user, args),
    'remove': lambda user, args, config: remove_plan(user, args),
    'share': lambda user, args, config: share_plan(user, args),
    'unshare': lambda user, args, config: unshare_plan(user, args)
}


def handle_plan(user, args, config):
    USER_CHOICE_PLAN.get(args.command)(user, args, config)


@with_printing_exception
def add_plan(user_name, args):
    owners = [Owner(user_name, AccessLevels.EDIT.value)]
    if args.owners:
        owners += args.owners
    plan_id = queries.add_plan(
        user_name, args.title, args.description, args.category,
        args.priority, args.tasks, args.events, args.reminders, owners
    )
    print(plan_id)


def show_plan(user_name, args, config):
    try:
        plans = queries.get_plans(user_name, args.title, args.category,
                                  args.priority, args.status, args.id)
    except ObjectDoesNotFound as e:
        print(e)
        return

    show_plan_table(plans, config)


@with_printing_exception
def check_plan(user_name, args):
    queries.check_plans(user_name, args.title, args.category,
                        args.priority, args.status, args.id)


@with_printing_exception
def edit_plan(user_name, args):
    queries.edit_plan(user_name, args.id, args.title, args.description,
                      args.category, args.priority)


@with_printing_exception
def remove_plan(user_name, args):
    queries.remove_plan(user_name, args.id)


@with_printing_exception
def share_plan(user_name, args):
    queries.add_owners_to_plan(user_name, args.id, args.owners)


@with_printing_exception
def unshare_plan(user_name, args):
    queries.remove_owners_from_plan(user_name, args.id, args.owners)
