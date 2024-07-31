from rest_framework import viewsets, status
from rest_framework.response import Response
from ..services.token import get_spotify_token

class SpotifyTokenView(viewsets.ViewSet):    
    def list(self, request):
        try:
            access_token = get_spotify_token()
            return Response({'access_token': access_token})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
