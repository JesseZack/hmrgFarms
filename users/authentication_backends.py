import os
import firebase_admin
from django.utils import timezone
from firebase_admin import credentials, auth
from rest_framework import authentication

from users.exceptions import InvalidAuthToken, NoAuthToken, FirebaseError
from users.models import CustomUser

cred = credentials.Certificate({
  "type": "service_account",
  "project_id": os.getenv('FIREBASE_PROJECT_ID'),
  "private_key_id": os.getenv('FIREBASE_PRIVATE_KEY_ID'),
  "private_key": os.getenv('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),
  "client_email": os.getenv('FIREBASE_CLIENT_EMAIL'),
  "client_id": os.getenv('FIREBASE_CLIENT_ID'),
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": os.getenv('FIREBASE_CLIENT_X509_CERT_URL'),
  "universe_domain": "googleapis.com"
})



class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            raise NoAuthToken('No Auth token provided')

        id_token = auth_header.split(' ').pop()
        decoded_token = None
        try:
            decoded_token = auth.verify_id_token(id_token)
        except Exception:
            raise InvalidAuthToken('Invalid auth token')

        if not id_token or not decoded_token:
            return None

        try:
            uid = decoded_token.get("uid")
        except Exception:
            raise FirebaseError()

        user, created = CustomUser.objects.get_or_create(username=uid)
        user.profile.last_activity = timezone.localtime()

        return user, None
