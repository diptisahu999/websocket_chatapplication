# from channels.consumer import SyncConsumer,AsyncConsumer
# from time import sleep
# from channels.exceptions import StopConsumer

# class Mysonsumer(SyncConsumer):
    

#     def websocket_connect(self,event):
#         print("Websocket connected!!!",event)
#         self.send({
#             'type':'websocket.accept'
#         })

#     def websocket_receive(self,event):
#         print("websocket Receive!!!",event)
#         print("websocket Receive!!!",event['text'])
        # self.send({
        #     'type':'websocket.accept',
        #     'text':'message send to clint'
        # })
        # for i in range(10):
        #     self.send({
        #     'type':'websocket.accept',
        #     'text': str(i)
        # })
        # sleep(1)

    # def websocket_disconnect(self,event):
    #     print("websocket disconnect!!!",event)
    #     raise StopConsumer()
        



# class MyAsysonsumer(AsyncConsumer):
#     async def websocket_connect(self,event):
#         print("Websocket connected!!!",event)
        #   await self.send({
        #     'type':'websocket.accept'
        #   })

#     async def websocket_receive(self,event):
#         print("websocket Receive!!!")

#     async def websocket_disconnect(self,event):
#         print("websocket disconnect!!!")



import json
from channels.generic.websocket import AsyncWebsocketConsumer,SyncConsumer
from .models import chat,Group
from asgiref.sync import async_to_sync


class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_box_name = self.scope["url_route"]["kwargs"]["chat_box_name"]
        self.group_name = "chat_%s" % self.chat_box_name

        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]

        # group=Group.objects.get(name=self.chat_box_name)
        # chats=chat(content=text_data_json['message'],group=group)
        # chats.save()

        
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chatbox_message",
                "message": message,
                "username": username,
            },
        )

    async def chatbox_message(self, event):
        message = event["message"]
        username = event["username"]

        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "username": username,
                }
            )
        )
         
    pass


# class ChatRoomConsumer(SyncConsumer):
#     def connect(self):
#         self.chat_box_name = self.scope["url_route"]["kwargs"]["chat_box_name"]
#         self.group_name = "chat_%s" % self.chat_box_name

#         self.channel_layer.group_add(self.group_name, self.channel_name)

#         self.accept()

#     def disconnect(self, close_code):
#         self.channel_layer.group_discard(self.group_name, self.channel_name)

#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json["message"]
#         username = text_data_json["username"]

#         # group=Group.objects.get(name=self.chat_box_name)
#         # chats=chat(content=text_data_json['message'],group=group)
#         # chats.save()

        
#         self.channel_layer.group_send(
#             self.group_name,
#             {
#                 "type": "chatbox_message",
#                 "message": message,
#                 "username": username,
#             },
#         )

#     def chatbox_message(self, event):
#         message = event["message"]
#         username = event["username"]

#         self.send(
#             text_data=json.dumps(
#                 {
#                     "message": message,
#                     "username": username,
#                 }
#             )
#         )
#     pass