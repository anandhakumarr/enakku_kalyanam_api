import json
from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import WebsocketConsumer
from api.models import Message, MessageRoom
from django.contrib.auth.models import User

class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        messages = Message.objects.filter(message_room=self.room).order_by('-created_ts').all()[:100]
        content = {
        'command': 'messages',
        'messages': self.messages_to_json(messages)
        }
        self.send_message(content)

    def new_message(self, data):
        content = data['content']
        message = Message.objects.create(message_room=self.room, content=content)
        content = {
        'command': 'new_message',
        'message': self.message_to_json(message)
        }
        self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            'user1_name': message.message_room.user1.first_name,
            'user2_name': message.message_room.user2.first_name,
            'user1': message.message_room.user1.username,
            'user2': message.message_room.user2.username,
            'room': str(message.message_room.id),
            'content': message.content,
            'created_at': str(message.created_ts)
        }


    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room = MessageRoom.objects.filter(id=self.room_id).first()
        if self.room:
            self.room_group_name = 'chat_%s' % self.room_id

            # Join room group
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )
            self.accept()
        else:
            self.close()

    def disconnect(self, close_code):
        # leave group room
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def send_chat_message(self, message):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps(message))
