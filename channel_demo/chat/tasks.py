from __future__ import absolute_import

from asgiref.sync import async_to_sync
from celery import shared_task
import time

from channels.layers import get_channel_layer


@shared_task
def hello_world():
  channel_layer = get_channel_layer()
  async_to_sync(channel_layer.group_send)(
    'chat_test',  # 构造Channels组名称
    {
      "type": "broadcast_message",
      "message": 'system time :'+str(time.time()),
    }
  )

