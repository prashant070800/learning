import json
from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.consumer import SyncConsumer, AsyncConsumerAdd
# from channels.exceptions import StopConsumer
class CallConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print("WebSocket Connected")

    async def disconnect(self, close_code):
        print("WebSocket Disconnected")

    async def receive(self, text_data):
        data = json.loads(text_data)
        print("Received audio stream data:", data)
        # Process or forward the stream




# class MySyncConsumer(SyncConsumer):
#     def websocket_connect(self, event):
#         print('Websocket Connected...', event)
#         self.send({
#             'type':'websocket.accept'
#         })

#     def websocket_receive(self, event):
#         print('Message Received...', event)
#         print('Message is', event['text'])

#     def websocket_disconnect(self, event):
#         print('Websocket Disconnected...', event)
#         raise StopConsumer()


# class MyAsyncConsumer(AsyncConsumer):
#     async def websocket_connect(self, event):
#         print('Websocket Connected...', event)
#         await self.send({
#             'type':'websocket.accept'
#         }) 

#     async def websocket_receive(self, event):
#         print('Message Received...', event)

#     async def websocket_disconnect(self, event):
#         print('Websocket Disconnected...', event)
#         raise StopConsumer()