from asyncio.windows_events import NULL
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from django.db.models.lookups import IsNull

from rest_framework.fields import NullBooleanField
from .models import Message, Chat, Contact
from .views import get_last_10_messages, get_reply_message, get_user_contact, get_current_chat,get_unseen_messages

User = get_user_model()


class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        messages = get_last_10_messages(data['chatId'])#,data['id'])
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        print(content)
        return self.send_message(content)

    def fetch_unseen_messages(self,data):
        user_contact = get_user_contact(data['from'])
        messages=get_unseen_messages(data['chatId'],user_contact)
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        print(content)
        return    self.send_message(content)

    def new_message(self, data):
        user_contact = get_user_contact(data['from'])
        if 'reply' in data:
            message = Message.objects.create(
            contact=user_contact,
            reply=get_reply_message(data['chatId'],data['reply']),
            content=data['message'])
        else:
            message = Message.objects.create(
            contact=user_contact,
            content=data['message'])
        current_chat = get_current_chat(data['chatId'])
        current_chat.messages.add(message)
        current_chat.save()
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

    def set_seen_messages(self,data):
        contact_user=get_user_contact(data['from'])
        messages=get_unseen_messages(data['chatId'],contact_user)
        print(messages)
        for msg in messages:
            msg.flag=True
            msg.save(update_fields=['flag'])
            print(msg)
        
    def flag_message(self,data):
        message=get_reply_message(data['chatId'],data['id'])
        message.flag=True
        message.save(update_fields=['flag'])

    def edit_message(self, data):
        message=get_reply_message(data['chatId'],data['id'])
        message.content=data['message']
        message.save(update_fields=['content'])
    
    def delete_message(self, data):
        message=get_reply_message(data['chatId'],data['id'])
        message.delete()


    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        if message.reply is None:
            return {
                'id': message.id,
                'author': message.contact.user.username,
                'content': message.content,
                'timestamp': str(message.timestamp)
        }
        else:
            return {
                'id': message.id,
                'author': message.contact.user.username,
                'content': message.content,
                'timestamp': str(message.timestamp),
                'reply':message.reply.content
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message,
        'edit_message': edit_message,
        'delete_message':delete_message,
        'set_flag':flag_message,
        'fetch_unseen_messages':fetch_unseen_messages,
        'set_seen_messages':set_seen_messages
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))
