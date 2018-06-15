# nxtodo-lib
nxtodo - is a simple python library that will allow you to create applications
like todos. Users, tasks, events, plans, reminders -q store them in the
database and manage them as you want.
##Getting Started
nxtodo depends on a [PostgreSQL](https://www.postgresql.org/), open source 
object-relational database. Please, [install](https://www.postgresql.org/download/) 
it before using nxtodo. 
###Installing
Clone repository from bitbucket:
```
$ git clone https://kharivitalij@bitbucket.org/kharivitalij/nxtodo.git
```
Install using pip3:
```
$ pip3 install nxtodo/nxtodo-lib/dist/nxtodo-1.0.tar.gz
```
###Initializing
After downloading and installing PostgreSQL, you should initialize the nxtodo:

For default:
```python
>> nxtodo.initialize()
```
For a more advanced configuration, use function with arguments:
```python
>> initialize(
            psql_user='nxtodo',
            psql_password='todotodo',
            psql_db_name='nxtodo',
            settings_module='nxtodo.configuration.settings'
          )
```      
\**settings_module* - is a django [settings](https://docs.djangoproject.com/en/1.11/ref/settings/) module:
###Configuration
If you want to use **already existing** database, you should only configure nxtodo:
```python
>> nxtodo.configure()
```
or
```python
>> nxtodo.configure('your_settings_module')
```
##Simple examples
Here you can find some simple examples to get you started.
```python
>> import nxtodo
>> nxtodo.configure()
>> from nxtodo import queries
```
###Adding task
```python
>> queries.add_task('creator', 'simple_task')
```
###Task with owners
```python
>> from nxtodo.thirdparty import Owner, AccessLevels
>> owners = [
    Owner('user_1', AccessLevels.EDIT.value),
    Owner('user_2', AccessLevels.READONLY.value)
  ]
>> queries.add_task('creator', 'task_with_owners', owners=owners)
```
\* *note, that owners 'user_1' and 'user_2' must be existing nxtodo users.*
###Getting tasks of user 'user_1'
```python
>> queries.get_tasks('user_1')
<QuerySet [<Task: task_1>]>
```
And some filters:
```python
>> queries.get_tasks('user_1', category='sport', priority=2)
<QuerySet [<Task: do_exercises>]>
```
###Adding subtasks
```python
>> queries.add_subtasks('user_1', to_task, [subtask1, subtask2 ...])
```
###Create a reminder for 'user_1', which can remind in a week before deadline with a periodicity of one day and also remind 2018/06/07 at 17:00:00
```python
>> queries.add_reminder(
    'user_1',
    start_remind_before=timedelta(weeks=1),
    datetimes=[datetime(2018, 6, 7, 17)],
    interval=timedelta(hours=1)
  )
>> queries.add_reminders_to_task('user_1', task_1_id, [reminder_1, ...])
```
And this same reminder to another task:
```
>> queries.add_reminders_to_task('user_1', task_2_id, [reminder_1, ...])
```
###Getting notification from tasks, events
```python
>> queries.check_tasks('user_1')
>> queries.check_events('user_1')
```
###And a bit more interesting:
Create a plan by 'user_1', which will create common for users 'user_2'
    and 'user_3' task 'task_1' and event 'event_1' from 2018/06/10 10:00
    to 2018/07/20 20:30 with a periodicity of 8 hours, and on weekends.
```python
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
```
##Running the tests
First, you need to initialize the database for tests:
```
$ python3
```
```python
>> import nxtodo
>> nxtodo.initialize(settings_module=nxtodo.configuration.settings_for_tests)
```
Run all tests for nxtodo:
```
$ python -m unittest discover nxtodo/nxtodo-lib/nxtodo/tests/ -v
```
#nxtodo_cli
nxtodo_cli - is a console client for nxtodo library.





