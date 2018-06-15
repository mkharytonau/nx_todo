"""
nxtodo - is a simple python library that will allow you to create applications
like todos. Users, tasks, events, plans, reminders -q store them in the
database and manage them as you want.

nxtodo depends on a PostgreSQL, open source object-relational database. You can
find instructions for downloading and installing PostgreSQL by this link:
https://www.postgresql.org/

After downloading and installing PostgreSQL, you should initialize the nxtodo:

    for default:
        >> nxtodo.initialize()

    for a more advanced configuration, use function with arguments:
        >> initialize(
            psql_user='nxtodo',
            psql_password='todotodo',
            psql_db_name='nxtodo',
            settings_module='nxtodo.configuration.settings'
          )
        * settings_module - is a django settings module:
        https://docs.djangoproject.com/en/1.11/ref/settings/

If you want to use already existing database, you should only configure nxtodo:

    >> nxtodo.configure()
    or
    >> nxtodo.configure('your_settings_module')

After this commands you available to use nxtodo fully!

Simple examples:

    >> import nxtodo
    >> nxtodo.configure()
    >> from nxtodo import queries

    a) Adding task:
        >> queries.add_task('creator', 'simple_task')

    b) Task with owners:
        >> from nxtodo.thirdparty import Owner, AccessLevels
        >> owners = [
            Owner('user_1', AccessLevels.EDIT.value),
            Owner('user_2', AccessLevels.READONLY.value)
          ]
        >> queries.add_task('creator', 'task_with_owners', owners=owners)
        * note, that owners 'user_1' and 'user_2' must be existing nxtodo users.

    c) Getting tasks of user 'user_1':
        >> queries.get_tasks('user_1')
        <QuerySet [<Task: task_1>]>
           and some filters:
        >> queries.get_tasks('user_1', category='sport', priority=2)
        <QuerySet [<Task: do_exercises>]>

    d) Adding subtasks:
        >> queries.add_subtasks('user_1', to_task, [subtask1, subtask2 ...])

    e) Create a reminder for 'user_1', which can remind in a week before deadline
       with a periodicity of one day and also remind 2018/06/07 at 17:00:00:
        >> queries.add_reminder(
            'user_1',
            start_remind_before=timedelta(weeks=1),
            datetimes=[datetime(2018, 6, 7, 17)],
            interval=timedelta(hours=1)
          )
        >> queries.add_reminders_to_task('user_1', task_1_id, [reminder_1, ...])
           and this same reminder to another task:
        >> queries.add_reminders_to_task('user_1', task_2_id, [reminder_1, ...])

    f) Getting notification from tasks, events:
        >> queries.check_tasks('user_1')
        >> queries.check_events('user_1')

    And a bit more interesting:

    g) Create a plan by 'user_1', which will create common for users 'user_2'
    and 'user_3' task 'task_1' and event 'event_1' from 2018/06/10 10:00
    to 2018/07/20 20:30 with a periodicity of 8 hours, and on weekends:
        >> queries.add_reminder(
            'user_1',
            start_remind_from=datetime(2018, 6, 10, 10),
            stop_remind_in=datetime(2018, 7, 20, 20, 30),
            interval=timedelta(hours=8),
            weekdays=[5, 6]
          )
        >> queries.add_plan(
            'user_1',
            'interesting_plan',
            tasks=[task_1, ...],
            events=[event_1, ...],
            owners=[
               Owner('user_1', 'edit'),
               Owner('user_1', 'edit')
            ],
            reminders=[reminder_1, ...]
          )
        >> queries.check_plans('user_2')
"""


from nxtodo.configuration.configuration import (
    initialize,
    configure,
    get_logger
)