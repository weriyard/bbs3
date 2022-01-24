class InboxException(Exception):
    pass


class InboxChangeTopicError(InboxException):
    pass


class InobxAddReplyError(InboxException):
    pass


class InboxWrongCredentials(InboxException):
    pass
