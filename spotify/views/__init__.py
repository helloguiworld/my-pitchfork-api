from rest_framework import views, viewsets,status, serializers
from rest_framework.response import Response
from django.utils import timezone
from ..services.token import get_spotify_token, execute_spotify_with_token_retry
from ..services.search import search_albums, old_searches
from ..services.album import get_album, old_albums
from ..services.client import get_client_ip
from ..exceptions import SpotifyResponseException
from common.permissions import IsSafe, IsMyOrigin


from ..models import Search, Album
from ..serializers import SearchSerializer, AlbumSerializer


class SpotifyTokenView(views.APIView):    
    def get(self, request):
        try:
            access_token = get_spotify_token()
            return Response({'access_token': access_token})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SpotifySearchView(views.APIView):
    permission_classes = [IsSafe, IsMyOrigin]
    
    def get(self, request):
        q = request.query_params.get('q', '')

        try:
            search_result = execute_spotify_with_token_retry(search_albums, q)
            return Response(search_result)
        except SpotifyResponseException as e:
            return Response(e.data, status=e.response.status_code)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SpotifyAlbumView(views.APIView):
    permission_classes = [IsSafe, IsMyOrigin]
    
    def get(self, request, id):
        try:
            album = execute_spotify_with_token_retry(get_album, id)
            return Response(album)
        except SpotifyResponseException as e:
            return Response(e.data, status=e.response.status_code)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ClientIpView(views.APIView):
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
   
class OldConsultSerializer(serializers.Serializer):
    days = serializers.IntegerField(required=False, default=1)
    detailed = serializers.BooleanField(required=False, default=False)
    clean = serializers.BooleanField(required=False, default=False)
    
class OldSearchesViewSet(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        serializer = OldConsultSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        days = serializer.validated_data['days']
        detailed = serializer.validated_data['detailed']
        clean = serializer.validated_data['clean']

        response_data = old_searches(days, detailed, clean)

        return Response(response_data)


class OldAlbumsViewSet(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        serializer = OldConsultSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        days = serializer.validated_data['days']
        detailed = serializer.validated_data['detailed']
        clean = serializer.validated_data['clean']

        response_data = old_albums(days, detailed, clean)

        return Response(response_data)
