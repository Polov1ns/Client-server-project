from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import exception_handler


class DomainError(APIException):
  """Базовий клас для бізнес-винятків"""

  pass


class NotFoundError(DomainError):
  status_code = status.HTTP_404_NOT_FOUND
  default_detail = 'Resource not found'
  default_code = 'not_found'


class ConflictError(DomainError):
  status_code = status.HTTP_409_CONFLICT
  default_detail = 'Resource conflict'
  default_code = 'conflict'


class BusinessValidationException(DomainError):
  status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
  default_detail = 'Business rule violation'
  default_code = 'business_validation_error'


def custom_exception_handler(exc, context):
  response = exception_handler(exc, context)
  request = context.get('request')
  path = request.path if request else 'unknown'

  if isinstance(exc, DomainError):
    detail_msg = exc.detail
    if isinstance(detail_msg, list):
      detail_msg = detail_msg[0]
    return Response(
        {
            'title': 'Business rule violation',
            'status': exc.status_code,
            'detail': str(detail_msg),
            'instance': path,
        },
        status=exc.status_code,
    )

  if response is None:
    return Response(
        {
            'title': 'An unexpected error occurred',
            'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
            'detail': 'The server could not complete the request.',
            'instance': path,
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )

  if response.status_code == status.HTTP_400_BAD_REQUEST:
    response.data = {
        'title': 'Validation error',
        'status': status.HTTP_400_BAD_REQUEST,
        'errors': response.data,
        'instance': path,
    }

  return response