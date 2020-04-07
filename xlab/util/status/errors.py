from xlab.util.status import error_codes_pb2


class GenericError(Exception):
    """Base class of errors reported by Google APIs.
  Attributes:
    code: Error code classifying the error, matching C++ StatusCode.
  """


class CancelledError(GenericError):
    code = error_codes_pb2.CANCELLED


class UnknownError(GenericError):
    code = error_codes_pb2.UNKNOWN


class InvalidArgumentError(GenericError):
    code = error_codes_pb2.INVALID_ARGUMENT


class DeadlineExceededError(GenericError):
    code = error_codes_pb2.DEADLINE_EXCEEDED


class NotFoundError(GenericError):
    code = error_codes_pb2.NOT_FOUND


class AlreadyExistsError(GenericError):
    code = error_codes_pb2.ALREADY_EXISTS


class PermissionDeniedError(GenericError):
    code = error_codes_pb2.PERMISSION_DENIED


class UnauthenticatedError(GenericError):
    code = error_codes_pb2.UNAUTHENTICATED


class ResourceExhaustedError(GenericError):
    code = error_codes_pb2.RESOURCE_EXHAUSTED


class FailedPreconditionError(GenericError):
    code = error_codes_pb2.FAILED_PRECONDITION


class AbortedError(GenericError):
    code = error_codes_pb2.ABORTED


class OutOfRangeError(GenericError):
    code = error_codes_pb2.OUT_OF_RANGE


class UnimplementedError(GenericError):
    code = error_codes_pb2.UNIMPLEMENTED


class InternalError(GenericError):
    code = error_codes_pb2.INTERNAL


class UnavailableError(GenericError):
    code = error_codes_pb2.UNAVAILABLE


class DataLossError(GenericError):
    code = error_codes_pb2.DATA_LOSS
