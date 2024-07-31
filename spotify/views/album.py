from rest_framework import viewsets, status
from rest_framework.response import Response
from common.permissions import IsSafe, IsMyOrigin
from ..services.token import execute_spotify_with_token_retry
from ..services.album import get_album
from ..exceptions import SpotifyResponseException

class SpotifyAlbumView(viewsets.ViewSet):
    permission_classes = [IsSafe, IsMyOrigin]
    
    def retrieve(self, request, pk=None):
        try:
            album = execute_spotify_with_token_retry(get_album, pk)
            return Response(album)
        except SpotifyResponseException as e:
            return Response(e.data, status=e.response.status_code)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
