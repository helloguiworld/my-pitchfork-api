from rest_framework import viewsets, serializers
from rest_framework.response import Response
from ..services.search import old_searches
from ..services.album import old_albums

class OldConsultSerializer(serializers.Serializer):
    days = serializers.IntegerField(required=False, default=1)
    detailed = serializers.BooleanField(required=False, default=False)
    clean = serializers.BooleanField(required=False, default=False)

class OldSearchesViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = OldConsultSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        days = serializer.validated_data['days']
        detailed = serializer.validated_data['detailed']
        clean = serializer.validated_data['clean']

        response_data = old_searches(days, detailed, clean)

        return Response(response_data)

class OldAlbumsViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = OldConsultSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        days = serializer.validated_data['days']
        detailed = serializer.validated_data['detailed']
        clean = serializer.validated_data['clean']

        response_data = old_albums(days, detailed, clean)

        return Response(response_data)
