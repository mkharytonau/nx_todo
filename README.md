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
settings_module - is a django [settings](https://docs.djangoproject.com/en/1.11/ref/settings/) module:
 
    
        
        
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




