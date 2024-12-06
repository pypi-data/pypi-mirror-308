from abc import ABC

from griff.infrastructure.bus.command.abstract_command import AbstractCommandResponse


class ErrorResponse(AbstractCommandResponse, ABC):
    def __init__(self):
        super(ErrorResponse, self).__init__(
            code=500, msg="System error occurred", linked_events=[]
        )
