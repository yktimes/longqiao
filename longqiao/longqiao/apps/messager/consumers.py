
# 注意　这里没用到前后段分离的，稍后理解了自己换成前后段分离的
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer,AsyncJsonWebsocketConsumer

import json


class MessagesConsumer(AsyncWebsocketConsumer):
    """处理私信应用中的ｗｅｂｓｏｃｋｅｔ请求"""



    async def connect(self):
        if self.scope['user'].is_anonymous:
            # 如果是匿名用户
            await self.close()

        else:
            # 加入聊天组
            await self.channel_layer.group_add(self.scope['user'].pk,self.channel_name)
            await self.accept()


    async def receive(self, text_data=None, bytes_data=None):
        """接受私信"""
        await self.send(text_data=json.dumps(text_data))


    async  def disconnect(self, code):
        """离开聊天组"""
        await self.channel_layer.group_discard(self.scope['user'].pk,self.channel_name)



















#


'''
class MyConsumer(WebsocketConsumer):
    
    def connect(self):
        self.accept(subprotocol='my protocol')
    
    def receive(self, text_data=None, bytes_data=None):
        pass
    
    
    def disconnect(self, code):
        pass
        
        
        
        '''