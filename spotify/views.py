from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services.token import get_spotify_token, execute_spotify_with_token_retry
from .services.search import search_albums
from .services.album import get_album
from .services.client import get_client_ip
from .exceptions import SpotifyResponseException

from rest_framework.permissions import IsAdminUser

class SpotifyTokenView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        try:
            access_token = get_spotify_token()
            return Response({'access_token': access_token})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SpotifySearchView(APIView):
    def get(self, request):
        q = request.query_params.get('q', '')

        try:
            search_result = execute_spotify_with_token_retry(search_albums, q)
            return Response(search_result)
        except SpotifyResponseException as e:
            return Response(e.data, status=e.response.status_code)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SpotifyAlbumView(APIView):
    def get(self, request, id):
        try:
            album = execute_spotify_with_token_retry(get_album, id)
            return Response(album)
        except SpotifyResponseException as e:
            return Response(e.data, status=e.response.status_code)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ClientIpView(APIView):
    def get(self, request):
        try:
            client_ip = get_client_ip(request)
            
            data = {
                'message': 'Hello, world!',
                'client_ip': client_ip
            }
            
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
