from http.client import HTTPResponse

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

# Create your views here.
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json


def index(request):
    return render(request, 'chat/index.html', {})


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))  # mark_safe 不再进行转义
    })


def send_group_msg(request,room_name):
    message = request.GET.get("message")
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'chat_%s' % room_name,  # 构造Channels组名称
        {
            "type": "broadcast_message",
            "message": message,
        }
    )
    return JsonResponse({'code':0})
