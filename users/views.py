from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotAuthenticated

from .serializers import CustomUserSerializer

class AuthenticatedUserView(APIView):
    def get(self, request):
        if request.user and request.user.is_authenticated:
            userSerializer = CustomUserSerializer(request.user)
            return Response(userSerializer.data)
        raise NotAuthenticated()