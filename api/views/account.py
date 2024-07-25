from rest_framework import viewsets
from ..models import Account
from ..serializers import AccountSerializer
from ..permissions import IsAdminOrAccountOwner

class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    permission_classes = [IsAdminOrAccountOwner]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Account.objects.all()
        return Account.objects.filter(user=self.request.user)