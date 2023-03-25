from pydantic import BaseModel

PARSER_ERROR = {'code': 121, 'title': 'invalid-request'}


class ErrorSource(BaseModel):
    pointer: str = "parameter"
    parameter: str


class Error(BaseModel):
    code: int
    title: str
    detail: str
    source: ErrorSource
