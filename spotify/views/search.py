from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from common.permissions import IsSafe, IsMyOriginOrAdmin
from ..services.token import execute_spotify_with_token_retry
from ..services.search import search_albums
from ..exceptions import SpotifyResponseException

def _search_albums(q=None):
    if not q:
        return Response({'error': 'No search query'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        search_result = execute_spotify_with_token_retry(search_albums, q)
        return Response(search_result)
    except SpotifyResponseException as e:
        return Response(e.data, status=e.response.status_code)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SpotifySearchView(viewsets.ViewSet):
    permission_classes = [IsSafe, IsMyOriginOrAdmin]
    
    def list(self, request):
        q = request.query_params.get('q', '')
        return _search_albums(q)
    
    @action(detail=False, methods=['get'], url_path='(?P<q>[^/]+)')
    def search(self, request, q=None):
        return _search_albums(q)
