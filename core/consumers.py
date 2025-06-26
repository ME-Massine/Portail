import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Message, Utilisateur

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        
        if not self.user.is_authenticated:
            await self.close()
            return
        
        # Get the other user ID from the URL
        self.other_user_id = self.scope['url_route']['kwargs']['other_user_id']
        
        # Create a unique room name for this conversation
        user_ids = sorted([str(self.user.id), str(self.other_user_id)])
        self.room_name = f"chat_{user_ids[0]}_{user_ids[1]}"
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type', 'message')
        
        if message_type == 'message':
            content = text_data_json['content']
            other_user_id = text_data_json['other_user_id']
            
            # Save message to database
            message = await self.save_message(content, other_user_id)
            
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': {
                        'id': message.id,
                        'content': message.contenu,
                        'sender_id': message.expediteur.id,
                        'sender_name': f"{message.expediteur.first_name} {message.expediteur.last_name}",
                        'timestamp': message.date_envoi.isoformat(),
                    }
                }
            )

    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': message
        }))

    @database_sync_to_async
    def save_message(self, content, other_user_id):
        other_user = User.objects.get(id=other_user_id)
        return Message.objects.create(
            expediteur=self.user,
            destinataire=other_user,
            contenu=content
        ) 