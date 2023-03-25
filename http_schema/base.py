from __future__ import annotations

from typing import List, Tuple

from pydantic import BaseModel, error_wrappers

from utils.http_errors import Error, PARSER_ERROR, ErrorSource


class Base(BaseModel):
    @classmethod
    def parse_json_dataset(cls, dataset: dict | List[dict]) -> Tuple[bool, BaseModel | List[BaseModel]]:
        errors = []
        result = []
        if not isinstance(dataset, list):
            try:
                return True, cls(**dataset)
            except error_wrappers.ValidationError as e:
                errors += e.errors()
        else:
            for data in dataset:
                try:
                    result.append(cls(**data))
                except error_wrappers.ValidationError as e:
                    errors += e.errors()
        if errors:
            result = []
            error: dict
            for error in errors:
                result.append(
                    Error(
                        code=PARSER_ERROR['code'],
                        title=PARSER_ERROR['title'],
                        detail=error.get('msg', ''),
                        source=ErrorSource(parameter=','.join(error.get('loc', '')))
                    )
                )
            return False, result
        return True, result
