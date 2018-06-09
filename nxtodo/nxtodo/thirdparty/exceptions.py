class Looping(Exception):
    def __init__(self, msg):
        Looping.txt = msg


class CompletionError(Exception):
    def __init__(self, msg):
        CompletionError.txt = msg