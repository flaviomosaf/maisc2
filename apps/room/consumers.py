import json
from django.contrib.auth.models import User
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Room, Message
from sendc2.views import make_entity_recognize
from nltk.tokenize import word_tokenize

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        #message = data['message']

        dict_, message_temp3 = {}, ''
        message_temp1 = make_entity_recognize(data['message'])['message_with_ents']
        #message = make_entity_recognize(data['message'])['dict_message_ents']
        message_temp2 = word_tokenize(str(message_temp1).replace('[','').replace(']',''))

        for __, _ in enumerate(message_temp2):
            if message_temp2.index(_) == 0:
                message_temp3 = str(_).title()+' '
                dict_[__] = {'term':_, 'bgcolor':'transparent'}
                continue
            if _ == 'ACT':
                message_temp3 += '[ACT] '
                dict_[__] = {'term':'[ACT]', 'bgcolor':'primary'}
            elif _ == 'AGT':
                message_temp3 += '[AGT] '
                dict_[__] = {'term':'[AGT]', 'bgcolor':'danger'}
            elif _ == 'VHC':
                message_temp3 += '[VHC] '
                dict_[__] = {'term':'[VHC]', 'bgcolor':'success'}
            elif _ == 'PLC':
                message_temp3 += '[PLC] '
                dict_[__] = {'term':'[PLC]', 'bgcolor':'info'}
            elif _ == 'WEP':
                message_temp3 += '[WEP] '
                dict_[__] = {'term':'[WEP]', 'bgcolor':'warning'}
            elif _ == 'UNT':
                message_temp3 += '[UNT] '
                dict_[__] = {'term':'[UNT]', 'bgcolor':'secondary'}
            elif _ == 'DRT':
                message_temp3 += '[DRT] '
                dict_[__] = {'term':'[DRT]', 'bgcolor':'danger'}
            else: 
                message_temp3 += _+' '
                dict_[__] = {'term':_, 'bgcolor':'transparent'}

        print('\n\n\n')
        #print(message_temp1)
        #print(message_temp2)
        #print(message_temp3)
        #print(dict_)
        print('\n\n\n')

        message = message_temp3 #dict_ #message_temp3
        username = data['username']
        room = data['room']

        await self.save_message(username, room, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    @sync_to_async
    def save_message(self, username, room, message):
        user = User.objects.get(username=username)
        room = Room.objects.get(slug=room)
        Message.objects.create(user=user, room=room, content=message)

        