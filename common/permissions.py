from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrMyOriginOrReadOnly(BasePermission):
    """
    Permite acesso total para  ou origin mypitchfork.fun e apenas leitura (GET, HEAD, OPTIONS) para outros.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return (request.user and request.user.is_staff) or request.META.get('HTTP_ORIGIN') == 'https://mypitchfork.fun'