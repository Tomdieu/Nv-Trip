import asyncio
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from users.models import Vehicle

class UserConsumer(AsyncConsumer):

	async def websocket_connect(self, event):
		# print("connected",event)
		user = self.scope['user']
		# print(user)
		await self.update_user_status(user,'online')
		await self.send({
    	   	"type": "websocket.accept",
    	})

	async def websocket_receive(self, event):
		self.send({
			"type": "websocket.send",
			# "text": event["text"],
		})

		# print("recieve",event);

	async def websocket_disconnect(self, event):
    	# called when websocked disconnect

		# print('disconnected',event)
		user = self.scope['user']
		await self.update_user_status(user,'offline')

    	# self.send({
		# 	"type": "websocket.send",
		# 	"text": event["text"],
		# })

	@database_sync_to_async
	def update_user_status(self,user,status):
		"""
			Updates the user status.
			status can be one of the following status: 'online','offline' or 'away'
		"""

		return get_user_model().objects.filter(pk=user.pk).update(status=status)

class VehicleConsumer(AsyncConsumer):
    
	async def websocket_connect(self, event):
		# print("connected",event)
		vehicle_id = self.scope["url_route"]["kwargs"]["id"]
		await self.update_vehicle_status(vehicle_id,'online')
		await self.send({
    	   	"type": "websocket.accept",
    	})

	async def websocket_receive(self, event):
		self.send({
			"type": "websocket.send",
			# "text": event["text"],
		})

		# print("recieve",event);

	async def websocket_disconnect(self, event):
    	# called when websocked disconnect

		# print('disconnected',event)
		vehicle_id = self.scope["url_route"]["kwargs"]["id"]
		await self.update_vehicle_status(vehicle_id,'offline')

	@database_sync_to_async
	def update_vehicle_status(self,id,status):
		"""
			Updates the user status.
			status can be one of the following status: 'online','offline' or 'away'
		"""

		return Vehicle.objects.filter(pk=id).update(status=status)