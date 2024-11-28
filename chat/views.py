import redis
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

# Singleton para conexão Redis
redis_instance = None

def get_redis_connection():
    global redis_instance
    if redis_instance is None:
        redis_instance = redis.StrictRedis(
            host='red-ct301al2ng1s73ee57r0',
            port=6379,
            decode_responses=True
        )
    return redis_instance

class ViewChats(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        redis_conn = get_redis_connection()
        chat_keys = redis_conn.smembers('available_chats')
        chat_names = [key.replace('chat_', '') for key in chat_keys]
        return Response(chat_names, status=status.HTTP_200_OK)

    def http_method_not_allowed(self, request, *args, **kwargs):
        return Response({
            'detail': 'Method not allowed'
        }, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class DeleteChat(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, roomName, *args, **kwargs):
        redis_conn = get_redis_connection()
        room_group_name = f'chat_{roomName}'

        # Verifica se o chat existe e remove
        if redis_conn.sismember("available_chats", room_group_name):
            redis_conn.srem("available_chats", room_group_name)
            redis_conn.delete(room_group_name)  # Remove as mensagens armazenadas
            return Response({"success": f"Chat {roomName} deleted."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": f"Chat {roomName} not found."}, status=status.HTTP_404_NOT_FOUND)
        
    def http_method_not_allowed(self, request, *args, **kwargs):
        return Response({
            'detail': 'Method not allowed'
        }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
