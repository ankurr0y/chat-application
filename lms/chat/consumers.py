import json
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from django.utils import timezone
from .models import Messages
import threading

def eg(*args):
    Messages(sender=args[0], sent_date=args[1], message=args[2], course_id = args[3]).save()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.id = self.scope['url_route']['kwargs']['course_id']
        self.room_group_name = 'chat_%s' % self.id
        await self.channel_layer.group_add(self.room_group_name,self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        now = timezone.now()
        # print(text_data_json)
        # print(self.user)
        # print(now.isoformat())
        # print(self.id)
        #print(Messages(sender=self.user, sent_date=now.isoformat(), message=text_data_json['message'], course = self.id))
        threading.Thread(target=eg, args=(self.user, now.isoformat(), text_data_json['message'], self.id)).start()
        self.send(text_data=json.dumps({'message': message}))
        await self.channel_layer.group_send(self.room_group_name,{'type': 'chat_message','message': message,'user': self.user.username,'datetime': now.isoformat(),})

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))