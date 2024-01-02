from rest_framework import status
from rest_framework.exceptions import APIException


class NoAuthToken(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_code = 'no_auth_token'
    default_detail = 'No authentication token provided'


class InvalidAuthToken(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_code = 'invalid_token'
    default_detail = 'Invalid authenticationi token provided'


class FirebaseError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_code = 'no_firebase_uid'
    default_detail = 'The user provided with the auth token is not a valid firebase user, it has no FirebaseUID'
