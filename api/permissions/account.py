from rest_framework import permissions

class HasAccount(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'account')

class IsAccountOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'account')
    
    def has_object_permission(self, request, view, obj):
        return obj.account.user == request.user
    
class IsAdminOrAccountOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.user.is_staff: return True
        return obj.account.user == request.user