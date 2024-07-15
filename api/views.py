from rest_framework import viewsets
from .models import Share
from .serializers import ShareSerializer

class ShareViewSet(viewsets.ModelViewSet):
    queryset = Share.objects.all()
    serializer_class = ShareSerializer
    