from django.http import JsonResponse
import redis

# Conexão com o Redis
redis_instance = redis.StrictRedis(
    host='red-ct301al2ng1s73ee57r0',
    port=6379,
    decode_responses=True
)

def list_chats(request):
    # Recupera os chats armazenados no conjunto 'available_chats'
    chat_keys = redis_instance.smembers('available_chats')
    # Retorna apenas os nomes (removendo o prefixo 'chat_')
    chat_names = [key.replace('chat_', '') for key in chat_keys]
    return JsonResponse(chat_names, safe=False)
