from griff.domain.common_opcodes import CommonOpCode
from griff.exceptions import WError


class AggregateNotFoundError(WError):
    status_code = 404
    operational_code = CommonOpCode.AGGREGATE_NOT_FOUND
    message = "Aggregate not found, aborting"


class AggregateHydratationError(WError):
    status_code = 500
    operational_code = CommonOpCode.AGGREGATE_HYDRATATION_FAILED
    message = "Aggregate Hydratation failed, aborting"


class RepositoryActionUndefinedError(WError):
    status_code = 500
    operational_code = CommonOpCode.REPOSITORY_ACTION_UNDEFINED
    message = "Repository action undefined, impossible to continue"


class AggregatePersistenceError(WError):
    status_code = 500
    operational_code = CommonOpCode.AGGREGATE_PERSTENCE_FAILED
    message = "Aggregate persistence failed, aborting"


class AggregateValidationError(WError):
    status_code = 422
    operational_code = CommonOpCode.AGGREGATE_VALIDATION_FAILED
    message = "Aggregate validation failed, aborting"
