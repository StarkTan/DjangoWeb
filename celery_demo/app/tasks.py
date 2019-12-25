from __future__ import absolute_import
from celery_demo.celery import app
from celery import shared_task
import time

@app.task
def start_running(nums):
  print('***>%s<***' %nums)
  print('--->>开始执行任务<<---')
  for i in range(10):
    print('>>'*(i+1))
    time.sleep(1)
  print('>---任务结束---<')
  return True


@shared_task
def hello_world():
    print('执行定时任务：'+str(time.time()))
