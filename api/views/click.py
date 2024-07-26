from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Avg
from common import IsAdminOrPostOnly
from ..models import SearchClick, AlbumClick, ShareClick
from ..serializers import SearchClickSerializer, AlbumClickSerializer, ShareClickSerializer
from unidecode import unidecode

# def ranking(queryset, value_fields, count_field='count'):
#     values = queryset.values_list(*value_fields)
    
#     frequency = {}
#     for value in values:
#         normalized_value = unidecode(value).lower()
#         frequency[normalized_value] = frequency.get(normalized_value, 0) + 1

class SearchClickViewSet(viewsets.ModelViewSet):
    queryset = SearchClick.objects.all()
    serializer_class = SearchClickSerializer
    permission_classes = [IsAdminOrPostOnly]
    
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
    permission_classes = [IsAdminOrPostOnly]
    
    @action(detail=False, methods=['get'])
    def ranking(self, request):
        album_clicks_groups = (
            AlbumClick.objects
                .values('album_id', 'album_name')
                .annotate(
                    count=Count('album_id'),
                )
                .order_by('-count')
        )
        return Response(album_clicks_groups)

class ShareClickViewSet(viewsets.ModelViewSet):
    queryset = ShareClick.objects.all()
    serializer_class = ShareClickSerializer
    permission_classes = [IsAdminOrPostOnly]

    @action(detail=False, methods=['get'])
    def ranking(self, request):
        share_clicks_groups = (
            ShareClick.objects
                .values('album_id', 'album_name')
                .annotate(
                    count=Count('album_id'),
                    average_review_scores=Avg('review_score')
                )
                .order_by('-count')
        )
        return Response(share_clicks_groups)
