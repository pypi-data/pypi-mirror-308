class ErrorCode:
    aborted = 10
    already_exists = 6
    cancelled = 1
    data_loss = 15
    deadline_exceeded = 4
    failed_precondition = 9
    internal = 13
    invalid_argument = 3
    not_found = 5
    ok = 0
    out_of_range = 11
    permission_denied = 7
    resource_exhausted = 8
    unauthenticated = 16
    unavailable = 14
    unimplemented = 12
    unknown = 2


class ErrorException(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message


class DBException(ErrorException):
    def __init__(self, code, message):
        self.code = code
        self.message = message

class KeyException(ErrorException):
    def __init__(self, code, message):
        self.code = code
        self.message = message

class AuthException(ErrorException):
    def __init__(self, code, message):
        self.code = code
        self.message = message
