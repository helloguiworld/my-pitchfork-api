import os
import socket
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

class TestSMTPView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            sock = socket.create_connection(
                (os.environ["EMAIL_HOST"], int(os.environ["EMAIL_PORT"])),
                timeout=10
            )
            sock.close()
            return Response({"smtp": "OK"})
        except Exception as e:
            return Response(
                {
                    "smtp": "FAIL",
                    "error": str(e),
                },
                status=500,
            )
