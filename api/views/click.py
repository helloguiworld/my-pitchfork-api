from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models import SearchClick, AlbumClick
from ..serializers import SearchClickSerializer, AlbumClickSerializer
from unidecode import unidecode

class SearchClickViewSet(viewsets.ModelViewSet):
    queryset = SearchClick.objects.all()
    serializer_class = SearchClickSerializer
    
    @action(detail=False, methods=['get'])
    def ranking(self, request):
        search_clicks_qs = SearchClick.objects.values_list('q', flat=True)
        
        frequency = {}
        for q in search_clicks_qs:
            normalized_q = unidecode(q).lower()
            frequency[normalized_q] = frequency.get(normalized_q, 0) + 1
            
        sorted_frequency = sorted(frequency.items(), key=lambda item: item[1], reverse=True)
        
        return Response([{'q': q, 'count': count} for q, count in sorted_frequency])

class AlbumClickViewSet(viewsets.ModelViewSet):
    queryset = AlbumClick.objects.all()
    serializer_class = AlbumClickSerializer
    
    @action(detail=False, methods=['get'])
    def ranking(self, request):
        album_clicks = AlbumClick.objects.values_list('album_id', 'album_name')
        
        frequency = {}
        for album_click in album_clicks:
            album_id, album_name = album_click
            
            if album_id in frequency:
                frequency[album_id]['count'] += 1
            else:
                frequency[album_id] = {'count': 1, 'album_name': album_name}
            
        sorted_frequency = sorted(frequency.items(), key=lambda item: item[1]['count'], reverse=True)
        
        return Response([{
            'album_id': album_id,
            'album_name': info['album_name'],
            'count': info['count']
        } for album_id, info in sorted_frequency])
