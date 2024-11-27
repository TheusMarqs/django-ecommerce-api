import json
from channels.generic.websocket import AsyncWebsocketConsumer

import redis

# Conexão com o Redis (ajuste o host conforme necessário)
redis_instance = redis.StrictRedis(
    host='red-ct301al2ng1s73ee57r0',
    port=6379,
    decode_responses=True
)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Adicionar o canal ao grupo
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        
        # Recuperar mensagens antigas do Redis
        messages = redis_instance.lrange(self.room_group_name, 0, -1)
        for message in messages:
            decoded_message = json.loads(message)
            await self.send(text_data=json.dumps({
                'message': decoded_message['message'],
                'sender': decoded_message['sender'],
            }))

    async def disconnect(self, close_code):
        # Remover o canal do grupo
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Receber a mensagem do cliente WebSocket
        data = json.loads(text_data)
        message = data['message']
        sender = data['sender']
        
        # Salvar a mensagem no Redis
        redis_instance.rpush(self.room_group_name, json.dumps({'sender': sender, 'message': message}))

        # Enviar a mensagem para o grupo
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender,
            }
        )

    async def chat_message(self, event):
    # Enviar a mensagem recebida para os WebSockets conectados
        message = event['message']
        sender = event['sender']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
        }))

