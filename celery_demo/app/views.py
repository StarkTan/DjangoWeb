from django.shortcuts import render, HttpResponse

# Create your views here.
from django.views import View

from .tasks import start_running
import time


class IdexView(View):
    def get(self, request):
        print('>=====开始发送请求=====<')
        for i in range(10):
            print('>>', end='')
            time.sleep(0.1)
        start_running.delay('》》》》》我是传送过来的《《《《《')
        return HttpResponse('<h2> 请求已发送 </h2>')
