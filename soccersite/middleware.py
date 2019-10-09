from allauth_2fa.middleware import BaseRequire2FAMiddleware

class RequireStaff2FAMiddleware(BaseRequire2FAMiddleware):
    def require_2fa(self, request):
        # Superusers are require to have 2FA.
        return request.user.is_staff
