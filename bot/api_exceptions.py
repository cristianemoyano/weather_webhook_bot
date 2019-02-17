from rest_framework.exceptions import APIException


class ServiceUnavailable(APIException):
    status_code = 501
    default_detail = 'Internal error, try again later.'
    default_code = 'internal_error'
