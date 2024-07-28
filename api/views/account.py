from rest_framework import viewsets
from common.permissions import IsAdminOrPostOnly
from ..models import Account
from ..serializers import AccountSerializer

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAdminOrPostOnly]
    
    def perform_create(self, serializer):
        account = serializer.save()
        print(f'NEW ACCOUNT {account.user}')
        