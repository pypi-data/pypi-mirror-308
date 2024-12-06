from pydantic import BaseModel, StrictBool, StrictInt, StrictStr


class RunRequest(BaseModel):
    "The parameters of a 'run' request to a Container tool"

    tool_id: StrictStr
    container: StrictStr
    command: list[StrictStr]
    username: StrictStr
    password: StrictStr


class SignalRequest(BaseModel):
    """The parameters of a 'signal' request to a Container tool"""

    tool_id: StrictStr
    signal: StrictStr


class GetStdoutResponse(BaseModel):
    """The response of a 'get_stdout' request to a Container tool"""

    stdout: StrictStr


class GetStateResponse(BaseModel):
    """The response of a 'get_state' request to a Container tool"""

    running: StrictBool
    return_code: StrictInt | None = None
