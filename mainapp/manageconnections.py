from django.db import connection
from django.db import connections


def make_sure_mysql_usable():
    """
    Credit:
        https://github.com/speedocjx/db_platform/blob/master/myapp/include/inception.py#L14
    """
    # mysql is lazily connected to in django.
    # connection.connection is None means
    # you have not connected to mysql before
    if connection.connection and not connection.is_usable():
        # destroy the default mysql connection
        # after this line, when you use ORM methods
        # django will reconnect to the default mysql
        del connections._connections.default
