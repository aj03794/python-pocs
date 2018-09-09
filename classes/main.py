class StorageRoomListUseCase(object):

    def __init__(self, repo):
        self.repo = repo

    def execute(self, request_object):
        print('request object', request_object)
        if not request_object:
            print('asdfads')
            return ResponseFailure.build_from_invalid_request_object(request_object)
        try:
            storage_rooms = self.repo.list(filters=request_object.filters)
            return ResponseSuccess(storage_rooms)
        except Exception as exc:
            print('Something went wrong')
            print("{}: {}".format(exc.__class__.__name__, "{}".format(exc)))
            return ResponseFailure.build_system_error(
                "{}: {}".format(exc.__class__.__name__, "{}".format(exc)))


class ResponseSuccess(object):

    def __init__(self, value=None):
        self.value = value

    def __nonzero__(self):
        return True

    __bool__ = __nonzero__


class ResponseFailure(object):
    RESOURCE_ERROR = 'ResourceError'
    PARAMETERS_ERROR = 'ParametersError'
    SYSTEM_ERROR = 'SystemError'

    def __init__(self, type_, message):
        self.type = type_
        self.message = self._format_message(message)

    def _format_message(self, msg):
        if isinstance(msg, Exception):
            return "{}: {}".format(msg.__class__.__name__, "{}".format(msg))
        return msg
    
    @property
    def value(self):
        return {'type': self.type, 'message': self.message}

    def __nonzero__(self):
        return False

    __bool__ = __nonzero__

    @classmethod
    def build_resource_error(cls, message=None):
        return cls(cls.RESOURCE_ERROR, message)

    @classmethod
    def build_system_error(cls, message=None):
        print('asdfas')
        return cls(cls.SYSTEM_ERROR, message)

    @classmethod
    def build_parameters_error(cls, message=None):
        return cls(cls.PARAMETERS_ERROR, message)

    @classmethod
    def build_from_invalid_request_object(cls, invalid_request_object):
        print('HELLO')
        message = "\n".join(["{}: {}".format(err['parameter'], err['message'])
                             for err in invalid_request_object.errors])
        return cls.build_parameters_error(message)


x = StorageRoomListUseCase('some repo')
print(x.execute('some request object'))