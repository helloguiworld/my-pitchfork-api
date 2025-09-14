from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from urllib.parse import urlparse
from django.http import HttpResponse
from common.permissions import IsMyOriginOrAdmin

class ProxyView(APIView):
    permission_classes = [IsMyOriginOrAdmin]
    
    def get(self, request):
        target_url = request.GET.get("url")
        if not target_url:
            return Response({"error": "Missing 'url' parameter"}, status=status.HTTP_400_BAD_REQUEST)

        parsed = urlparse(target_url)
        if parsed.scheme not in ["http", "https"]:
            return Response({"error": "Invalid URL scheme"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            response = requests.get(target_url, stream=True, timeout=10)
            content_type = response.headers.get("Content-Type", "application/octet-stream")
            return HttpResponse(response.content, content_type=content_type, status=response.status_code)
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
