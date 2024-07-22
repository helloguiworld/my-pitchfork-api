from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotAuthenticated
from rest_framework import status

from .serializers import CustomUserSerializer as UserSerializer
from users.models import CustomUser as User

class AuthenticatedUserView(APIView):
    def get(self, request):
        if request.user and request.user.is_authenticated:
            userSerializer = UserSerializer(request.user)
            return Response(userSerializer.data)
        raise NotAuthenticated()


class PasswordResetRequestView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
            userSerializer = UserSerializer(user)
            return Response({"user": userSerializer.data})
        except User.DoesNotExist:
            return Response({"error": "User with this email does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        
        # token_generator = default_token_generator
        # current_site = get_current_site(request)
        # mail_subject = 'Password Reset Request'
        # message = render_to_string('password_reset_email.html', {
        #     'user': user,
        #     'domain': current_site.domain,
        #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        #     'token': token_generator.make_token(user),
        # })
        # send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [email])
        
        # return Response({"message": "Password reset link sent"}, status=status.HTTP_200_OK)