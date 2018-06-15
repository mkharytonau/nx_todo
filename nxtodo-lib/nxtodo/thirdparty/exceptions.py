class Looping(Exception):
    def __init__(self, msg):
        Looping.txt = msg


class CompletionError(Exception):
    def __init__(self, msg):
        CompletionError.txt = msg


class ObjectDoesNotFound(Exception):
    def __init__(self, msg):
        ObjectDoesNotFound.txt = msg


class NoNotifications(Exception):
    def __init__(self, msg):
        NoNotifications.txt = msg