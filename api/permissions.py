from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed


class CustomJWTAuthentication(JWTAuthentication):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if not user.is_active:
            raise AuthenticationFailed("User inactive or deleted!")
        return True
