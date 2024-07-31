from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotAuthenticated

from ..serializers import CustomUserSerializer as UserSerializer

class AuthenticatedUserView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            userSerializer = UserSerializer(request.user)
            return Response(userSerializer.data)
        raise NotAuthenticated()
