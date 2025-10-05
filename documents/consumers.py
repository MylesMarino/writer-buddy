import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Document


class DocumentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.document_id = self.scope['url_route']['kwargs']['document_id']
        self.room_group_name = f'document_{self.document_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')

        if message_type == 'content_update':
            content = data.get('content', '')
            await self.save_content(content)
            
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'content_broadcast',
                    'content': content,
                    'sender_channel': self.channel_name
                }
            )
        


    async def content_broadcast(self, event):
        if event['sender_channel'] != self.channel_name:
            await self.send(text_data=json.dumps({
                'type': 'content_update',
                'content': event['content']
            }))



    @database_sync_to_async
    def save_content(self, content):
        try:
            document = Document.objects.get(id=self.document_id)
            document.content = content
            document.save()
        except Document.DoesNotExist:
            pass
