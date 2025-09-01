from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from google.cloud import storage
import json
import os

class GCSJsonView(APIView):
    def get(self, request, platform):
        # key_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ayam-debugging-engagement-api-1bd6ccd512be.json')
        key_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'ayam-debugging-engagement-api-1bd6ccd512be.json')
        storage_client = storage.Client.from_service_account_json(key_path)
        bucket = storage_client.bucket('ayam_debugging')
        file_map = {
            'x': 'tweets.json',
            'instagram': 'instagram.json',
            # 'facebook': 'facebook_post.json'
        }
        filename = file_map.get(platform)
        if not filename:
            return Response({'error': 'Invalid platform'}, status=status.HTTP_400_BAD_REQUEST)
        blob = bucket.blob(filename)
        data = blob.download_as_text()
        json_data = json.loads(data)
        return Response(json_data, status=status.HTTP_200_OK)