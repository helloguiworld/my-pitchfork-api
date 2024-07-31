import os

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status, serializers

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail

from ..serializers import CustomUserSerializer as UserSerializer
from users.models import CustomUser as User
from common.permissions import IsMyOrigin

class PasswordResetRequestView(APIView):
    permission_classes = [IsMyOrigin]
    
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User with this email does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        
        token = default_token_generator.make_token(user)
        u_id = urlsafe_base64_encode(force_bytes(user.pk))
        base_url = "https://mypitchfork.fun/" if os.environ.get('PRODUCTION') else "http://localhost:8000/"
        
        password_reset_url = f"{base_url}users/password-reset/{u_id}/{token}/"
        
        subject = "Your myPitchfork Password Reset"
        email_template_name = "password_reset_email.txt"
        context = {
            "password_reset_url": password_reset_url,
        }
        email_content = render_to_string(email_template_name, context)
        
        try:
            send_mail(
                subject,
                email_content,
                'mypitchfork.fun@gmail.com',
                [email],
                fail_silently=False
            )
            print(f"PASSWORD RESET EMAIL SENT: {email}")
            if os.environ.get('PRODUCTION'):
                return Response({"success": "Password reset email sent"})
            else:
                return Response({"success": "Password reset email sent", "password_reset_url": password_reset_url})
        except Exception as e:
            print(f"FAIL TO SENT PASSWORD RESET EMAIL: {email}")
            print(f"ERROR: {e}")
            return Response({"error": "Failed to send password reset email"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)

class PasswordResetView(APIView):
    permission_classes = [IsMyOrigin]
    
    def post(self, request, u_id_b64, token):
        try:
            u_id = urlsafe_base64_decode(u_id_b64).decode()
            user = User.objects.get(pk=u_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            serializer = PasswordResetSerializer(data=request.data)
            if serializer.is_valid():
                new_password = serializer.validated_data['new_password']
                user.set_password(new_password)
                user.save()
                Token.objects.filter(user=user).delete()
                if os.environ.get('PRODUCTION'):
                    return Response({"success": "Password has been reset"})
                else:
                    return Response({"success": "Password has been reset", "username": user.username})
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Invalid token or user ID."}, status=status.HTTP_400_BAD_REQUEST)