from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(ex, context):
    response = exception_handler(ex, context)

    if isinstance(ex, IntegrityError):
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        data = {"status_code": status_code, "detail": "Resource already exists."}

        response = _update_response(response, status_code, data)

    return response


def _update_response(response, status_code, data):
    if response is None:
        return Response(status=status_code, data=data)
    else:
        response.status_code = status_code

        response.data["status_code"] = status_code
        response.data["detail"] = "Resource already exists."

        return response
