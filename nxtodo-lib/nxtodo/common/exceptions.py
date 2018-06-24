class Looping(Exception):
    """
    Looping exception, it serves to prevent cycling when
    subtasks are added to tasks.
    """
    def __init__(self, msg):
        Looping.txt = msg


class CompletionError(Exception):
    """
    CompletionError exception, it does not allow changing the status
    of the task to a "completed", when not all subtasks are completed.
    """
    def __init__(self, msg):
        CompletionError.txt = msg


class ObjectDoesNotFound(Exception):

    """
    ObjectDoesNotFound exception, this exception occurs when the objects
    where not found in the database
    """

    def __init__(self, msg):
        ObjectDoesNotFound.txt = msg


class NoNotifications(Exception):
    """
    NoNotifications exception, this exception occurs when there are
    no notifications to show.
    """
    def __init__(self, msg):
        NoNotifications.txt = msg