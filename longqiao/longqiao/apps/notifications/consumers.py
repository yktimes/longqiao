
# 注意　这里没用到前后段分离的，稍后理解了自己换成前后段分离的
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer,AsyncJsonWebsocketConsumer

import json


class MessagesConsumer(AsyncWebsocketConsumer):
    """处理的ｗｅｂｓｏｃｋｅｔ请求"""



    async def connect(self):
        if self.scope['user'].is_anonymous:
            # 如果是匿名用户，拒绝
            await self.close()

        else:
            # 加入 notifications 监听组
            await self.channel_layer.group_add("notifications",self.channel_name)
            await self.accept()


    async def receive(self, text_data=None, bytes_data=None):
        """讲接收到的消息返回给前端"""
        await self.send(text_data=json.dumps(text_data))


    async  def disconnect(self, code):
        """离"""
        await self.channel_layer.group_discard("notifications",self.channel_name)



















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