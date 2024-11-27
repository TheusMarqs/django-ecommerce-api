import redis
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

redis_instance = redis.StrictRedis(
    host='red-ct301al2ng1s73ee57r0',
    port=6379,
    decode_responses=True
)

class ViewChats(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        # Recupera os chats armazenados no conjunto 'available_chats'
        chat_keys = redis_instance.smembers('available_chats')
        chat_names = [key.replace('chat_', '') for key in chat_keys]
        return Response(chat_names, status=status.HTTP_200_OK)
        
    def http_method_not_allowed(self, request, *args, **kwargs):
        return Response({
            'detail': 'Method not allowed'
        },  status=status.HTTP_405_METHOD_NOT_ALLOWED)
        