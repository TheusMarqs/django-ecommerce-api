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
        
class DeleteChat(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, roomName, *args, **kwargs):
        
        room_group_name = f'chat_{roomName}'

    # Remover o chat do conjunto de chats disponíveis
    if redis_instance.sismember("available_chats", room_group_name):
        redis_instance.srem("available_chats", room_group_name)
        redis_instance.delete(room_group_name)  # Remove as mensagens armazenadas
        return JsonResponse({"success": f"Chat {roomName} deleted."})
    else:
        return JsonResponse({"error": f"Chat {roomName} not found."}, status=404)
        