from urllib.request import Request
import jwt

from django.conf import settings

from rest_framework import authentication, exceptions, permissions

from .models import Barber, Client


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Token'

    def authenticate(self, request):
        
        request.user = None
        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header:
            return None

        if len(auth_header) == 1:
            return None

        elif len(auth_header) > 2:
            return None

        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != auth_header_prefix:
            return None
        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except:
            msg = 'Invalid authentication. Could not decode token.'
            raise exceptions.AuthenticationFailed(msg)
        barber = None
        client = None
        try:
            barber = Barber.objects.get(pk=payload['id'])
        except Barber.DoesNotExist:
            try:
                client = Client.objects.get(pk=payload['id'])
            except Client.DoesNotExist:
                msg = 'No user matching this token was found.'
                raise exceptions.AuthenticationFailed(msg)

        if barber and not barber.is_active:
            msg = 'This user has been deactivated.'
            raise exceptions.AuthenticationFailed(msg)

        if client and not client.is_active:
            msg = 'This user has been deactivated.'
            raise exceptions.AuthenticationFailed(msg)

        obj = client if client else barber
        return obj, token

class IsStaffForReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.staff == True:
            return True
        elif request.user.staff == False and request.method in permissions.SAFE_METHODS:
            return True
        return False

class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.staff 
            