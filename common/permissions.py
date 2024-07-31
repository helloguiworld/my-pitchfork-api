import os
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsSafe(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS   

class IsMyOriginOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_staff:
            return True
        if os.getenv('PRODUCTION'):
            return request.META.get('HTTP_ORIGIN') == 'https://mypitchfork.fun'
        return True

class IsAdminOrPostOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_staff:
            return True
        return request.method == 'POST'
    