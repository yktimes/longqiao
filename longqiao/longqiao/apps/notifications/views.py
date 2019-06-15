from django.shortcuts import render

# Create your views here.

from . models import Notification
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class NotificationUnreadListView(LoginRequiredMixin, ListView):
    """未读通知列表"""
    model = Notification
    context_object_name = 'notification_list'
    template_name = 'notifications/notification_list.html'

    def get_queryset(self, **kwargs):
        return self.request.user.notifications.unread()


@login_required
def mark_all_as_read(request):
    """将所有通知标为已读"""
    request.user.notifications.mark_all_as_read()
    redirect_url = request.GET.get('next') # 如果从其他链接跳过来的



    if redirect_url:
        return redirect(redirect_url)

    return redirect('notifications:unread')



@login_required
def mark_as_read(request, slug):
    """根据slug标为已读"""
    notification = get_object_or_404(Notification, slug=slug)
    notification.mark_as_read()

    redirect_url = request.GET.get('next')



    if redirect_url:
        return redirect(redirect_url)

    return redirect('notifications:unread')


@login_required
def get_latest_notifications(request):
    """最近的未读通知"""
    notifications = request.user.notifications.get_most_recent()
    return render(request, 'notifications/most_recent.html',
                  {'notifications': notifications})


def notification_handler(actor, recipient, verb, action_object, **kwargs):
    """
    通知处理器
    :param actor:           request.user对象
    :param recipient:       User Instance 接收者实例，可以是一个或者多个接收者
    :param verb:            str 通知类别
    :param action_object:   Instance 动作对象的实例
    :param kwargs:          key, id_value等
    :return:                None
    """
    # TODO username 改成　pk　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　这里还有个问题　我写的是Ｃｕｓｅｒ
    if actor.username != recipient.username and recipient.username == action_object.Cuser.username:
        # 只通知接收者，即recipient == 动作对象的作者
        key = kwargs.get('key', 'notification')
        id_value = kwargs.get('id_value', None)
        # 记录通知内容
        Notification.objects.create(
            actor=actor,
            recipient=recipient,
            verb=verb,
            action_object=action_object
        )

        channel_layer = get_channel_layer()
        payload = {
            'type': 'receive', # 固定字段
            'key': key, # 这个是给前端的标记
            'actor_name': actor.username,
            'id_value': id_value
        }
        async_to_sync(channel_layer.group_send)('notifications', payload)