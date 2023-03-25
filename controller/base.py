import pydantic
from flask_restful import Resource
from functools import wraps


def exception_handling(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # try:
            response = func(*args, **kwargs)
            return response
        # except Exception as e:
        #     return {'server_message': str(e)}, 501
        #     todo: send mail

    return wrapper


class BaseResource(Resource):
    method_decorators = [exception_handling, ]

    def options(self, *args, **kwargs):
        return {}, 200

    def dispatch_request(self, *args, **kwargs):
        return super().dispatch_request(*args, **kwargs)
