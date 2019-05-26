from django.shortcuts import render
import base64

from django.shortcuts import render
from django.db.models import F
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.generics import CreateAPIView

from rest_framework.generics import DestroyAPIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView



# Create your views here.

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Message
from .serializers import MessageSerializer
from users.serializers import PostUserSerializer
from  users.models import User,FriendShip

class MessagesListView(APIView):


    # queryset = Message.objects.all()

    # serializer_class = MessageSerializer
    #
    # def list(self, request, *args, **kwargs):
    #     context ={}
    #
    #     # 获取除当前登录用户外的所有用户，按最近登录时间降序排列
    #     users_list = get_user_model().objects.filter(is_active=True).exclude(
    #         pk=self.request.user
    #     ).order_by('-last_login')[:10]
    #
    #
    #
    #
    #     # 最近一次私信互动的用户
    #     last_conversation = Message.objects.get_most_recent_conversation(self.request.user)
    #     context['active'] = last_conversation.username
    #     return Response({'last_conversation':context})

    def get(self,request):
        context = {}

        # 获取除当前登录用户外的所有用户，按最近登录时间降序排列
        users_list= User.objects.filter( pk=self.request.user.pk,is_active=True).exclude(
            pk=request.user.pk
        ).order_by('-last_login')
        lo=[]
        print(users_list)
        for u in users_list:
            lo.append(PostUserSerializer(u))
        context['user_list'] = lo
        # PostUserSerializer(users_list,many=True)
        active_user = Message.objects.get_most_recent_conversation(self.request.user)

        s = Message.objects.get_conversation(self.request.user, active_user)

        s = MessageSerializer(s)

        # 最近一次私信互动的用户
        last_conversation = Message.objects.get_most_recent_conversation(self.request.user)
        context['active'] = last_conversation.nickname


        return Response({'s': s.data,'last_conversation':context})

    # def get_queryset(self):
    #     """最近私信互动的内容"""
    #     active_user = Message.objects.get_most_recent_conversation(self.request.user)
    #
    #     s = Message.objects.get_conversation(self.request.user, active_user)
    #     return s


class ConversationListView(APIView):
    """与指定用户的私信内容"""

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super(ConversationListView, self).get_context_data()
    #     context['active'] = self.kwargs["username"]
    #     return context

    def get(self,request,pk):
        active_user = get_object_or_404(get_user_model(),
                                        pk=pk) # 获取用户　pk
        m = Message.objects.get_conversation(self.request.user, active_user)

        m= MessageSerializer(m)


        return Response({'s': m.data})
#
# @login_required
# @ajax_required
# @require_http_methods(["POST"])
# def send_message(request):
#     """发送消息，AJAX POST请求"""
#     sender = request.user
#     recipient_username = request.POST['to']
#     recipient = get_user_model().objects.get(username=recipient_username)
#     message = request.POST['message']
#     if len(message.strip()) != 0 and sender != recipient:
#         msg = Message.objects.create(
#             sender=sender,
#             recipient=recipient,
#             message=message
#         )
#
#     return render(request, 'messager/single_message.html', {'message': msg})
#
#     return HttpResponse()


class Send_message(APIView):

    permission_classes = [IsAuthenticated,]

    def post(self,request):


        """发送消息，AJAX POST请求"""
        sender = request.user
        recipient_pk = request.data['to']  # 获取用户　pk
        recipient = get_user_model().objects.get(pk=recipient_pk)
        message = request.data['message']
        if len(message.strip()) != 0 and sender != recipient:
            msg = Message.objects.create(
                sender=sender,
                recipient=recipient,
                message=message
            )

            channel_layer = get_channel_layer()
            payload = {
                'type': 'receive', # 固定字段
                'message': msg,
                'sender': sender.pk
            }
            # group_send(group: 所在组-接收者的pk, message: 消息内容)
            async_to_sync(channel_layer.group_send)(recipient.pk, payload) # 相当于装饰器

            return Response( {'message': msg})

        return HttpResponse()
