from django.conf import settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class FirebaseTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['sub'] = settings.SIMPLE_JWT.get("ISSUER", "")

        token['iat'] = token['exp'] - (60 * 60 * 24)

        token['claims'] = {'is_superuser': user.is_superuser, 'is_staff': user.is_staff}

        return token
