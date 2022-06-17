import asyncio
import json
from tkinter.messagebox import NO
from channels.consumer import AsyncConsumer
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer

from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from .models import DriverNotification, UserNotification
from django.db.models import Q

from users.models import Vehicle
from map.models import UserBookPlace
from map.models import DriverTransportPassenger

User = get_user_model()

class DriverNotificationsConsumer(WebsocketConsumer):
    def connect(self):
        
        id = self.scope["url_route"]["kwargs"]["id"]
        print(id)

        self.room_group_name = 'drive_'+str(id)
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def receive(self, text_data):
        text_data = json.loads(text_data)
        vehicleId = text_data['vehicleId'];
        sender = text_data['bookedId'];
        user = text_data['user']
        np = text_data['numberOfPlace']
        origin = text_data['origin']
        destination = text_data['destination']
        price = text_data['price']
        option =text_data['paymentOption']
        msg = f'The Passenger {user} Wants to book {np} places In your vehicle going from {origin} to {destination} Willing to pay {price} from {option}';
        duplicate = DriverNotification.objects.filter(Q(vehicle_id=vehicleId) & Q(sender_id=sender) & Q(msg=msg))
        print('Duplicates : ',duplicate)
        if not duplicate:
            notif = DriverNotification.objects.create(vehicle_id=vehicleId,sender_id=sender,msg=msg)
            text_data['notification_id'] = notif.pk
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type':'send_notification',
                    'message':text_data
                }
            )

    def send_notification(self,event):
        message = event['message']
        self.send(text_data=json.dumps({
            'type':'book_place',
            'message':message
        }))


class UserNotificationsConsumer(WebsocketConsumer):

    def connect(self):
        id = self.scope["url_route"]["kwargs"]["id"]
        async_to_sync(self.channel_layer.group_add)(f"user_{id}", self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        id = self.scope["url_route"]["kwargs"]["id"]
        async_to_sync(self.channel_layer.group_discard)(f"user_{id}", self.channel_name)

    def receive(self, text_data):
        id = self.scope["url_route"]["kwargs"]["id"]
        text_data = json.loads(text_data)
        ntype = text_data['type']
        print(ntype)
        userId = text_data['idUser']
        ntype = text_data['type']
        bookId = text_data['idBook']
        vehicleId = text_data['vehicleId']
        notification_id = text_data['notification_id']
        book = UserBookPlace.objects.get(id=vehicleId)
        veh = Vehicle.objects.get(id=vehicleId)
        msg = {}
        print(text_data)
        msg['message'] = "The Driver {} has accepted your book from {} to {} ".format(veh.user,book.origin,book.destination)

        if(ntype == 'book_accepted'):
            user = User.objects.get(id=userId)
            DriverNotification.objects.filter(id=notification_id).update(accepted=True)
            UserNotification.objects.create(user=user,msg=msg['message'],sender=veh)
            duplicates = DriverTransportPassenger.objects.filter(Q(booked_id=bookId) & Q(vehicle_id=vehicleId) &Q(accept='accept'))
            if not duplicates.exists():
                DriverTransportPassenger.objects.create(booked_id=bookId,vehicle_id=vehicleId,accept='accept')
                async_to_sync(self.channel_layer.group_send)(
                f"user_{id}",
                {
                    'type':'chat.message',
                    'message':text_data
                }
            )
        else:
            async_to_sync(self.channel_layer.group_send)(
                f"user_{id}",
                {
                    'type':'chat.message',
                    'message':json.dumps({'recieve':True})
                }
            )
        # async_to_sync(self.channel_layer.group_send)(
        #     f"user_{id}",
        #     {
        #         "type": "chat.message",
        #         "text": text_data,
        #     },
        # )

    def chat_message(self, event):
        # print(event['text'])
        self.send(text_data=json.dumps({
            'type':'accept',
            'message':event['text']
        }))