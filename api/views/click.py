from rest_framework import viewsets
from ..models import SearchClick
from ..serializers import SearchClickSerializer

class SearchClickViewSet(viewsets.ModelViewSet):
    queryset = SearchClick.objects.all()
    serializer_class = SearchClickSerializer