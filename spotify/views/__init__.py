from rest_framework import views, viewsets,status, serializers
from rest_framework.response import Response
from django.utils import timezone
from ..services.token import get_spotify_token, execute_spotify_with_token_retry
from ..services.search import search_albums
from ..services.album import get_album
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
    
class OldSearchsViewSet(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        # Recebe o número de dias da requisição POST
        serializer = OldConsultSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        days = serializer.validated_data['days']
        detailed = serializer.validated_data['detailed']

        # Calcula a data limite
        now = timezone.now()
        limit_date = now - timezone.timedelta(days=days)

        # # Apaga os registros mais antigos que a data limite
        # deleted_count, _ = Search.objects.filter(updated_at__lte=limit_date).delete()
        deleted_count = Search.objects.filter(updated_at__lte=limit_date)
        count = deleted_count.count()

        if detailed:
            s_s = SearchSerializer(deleted_count, many=True)
            return Response({'days': days, 'now': now, 'limit': limit_date, 'count': count, 'deleted': [s['q'] for s in s_s.data]})
        else:
            return Response({'days': days, 'now': now, 'limit': limit_date, 'count': count})
        # return Response({'message': f'{limit_date} searches deleted'})

class OldAlbumsViewSet(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        # Recebe o número de dias da requisição POST
        serializer = OldConsultSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        days = serializer.validated_data['days']
        detailed = serializer.validated_data['detailed']

        # Calcula a data limite
        now = timezone.now()
        limit_date = now - timezone.timedelta(days=days)

        # # Apaga os registros mais antigos que a data limite
        # deleted_count, _ = Search.objects.filter(updated_at__lte=limit_date).delete()
        deleted_count = Album.objects.filter(updated_at__lte=limit_date)
        count = deleted_count.count()

        if detailed:
            a_s = AlbumSerializer(deleted_count, many=True)
            return Response({'days': days, 'now': now, 'limit': limit_date, 'count': count, 'deleted': [a['name'] for a in a_s.data]})
        else:
            return Response({'days': days, 'now': now, 'limit': limit_date, 'count': count})
        # return Response({'message': f'{limit_date} searches deleted'})
            
