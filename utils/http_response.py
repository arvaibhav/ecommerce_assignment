from __future__ import annotations
from typing import Dict, List

from utils.http_errors import Error


def ok_response(response: Dict | List, http_code=200):
    return response, http_code


def error_response(errors: List[Error], http_code=400):
    return [error.dict() for error in errors], http_code
