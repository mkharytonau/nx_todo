"""
module contains
- default settings in 'settings.py' file
- settings for tests in 'sittings_for_tests.py' file

Function initialize() is used to initialize library:
-create a postgres user
-create a postgres database
-create tables in database that are requeried for nxtodo.

Function configure() is used to configure nxtodo to a specific database.

Function get_logger() returns a logger objects, which you can configure,
as you want.
"""

from nxtodo.configuration.configuration import (
    initialize,
    configure,
    get_logger
)