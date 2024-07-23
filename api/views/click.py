from rest_framework import viewsets
from ..models import SearchClick, AlbumClick
from ..serializers import SearchClickSerializer, AlbumClickSerializer

class SearchClickViewSet(viewsets.ModelViewSet):
    queryset = SearchClick.objects.all()
    serializer_class = SearchClickSerializer
    
class AlbumClickViewSet(viewsets.ModelViewSet):
    queryset = AlbumClick.objects.all()
    serializer_class = AlbumClickSerializer