from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
import json
from .models import Device
from .serializers import DeviceSerializer
# Create your views here.
from rest_framework import viewsets, mixins
from mqtt_client.apps import client

pub_pre = '/usi/cloud/config/'

class DeviceViewSet(mixins.UpdateModelMixin,
                     viewsets.ReadOnlyModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def perform_update(self, serializer):
        # 更新前修改部分数据
        instance = self.get_object()
        ver_arr = instance.version.split('.')
        serializer.validated_data['version'] = ver_arr[0]+'.'+str(int(ver_arr[1])+1)
        serializer.validated_data['confirm'] = False
        serializer.save()
        sn = serializer.data['id']
        # 推送数据
        client.publish(pub_pre + sn, json.dumps(Device.objects.get(id=sn).pub_msg()), qos=1)

    @action(methods=['GET'],detail=True)
    def config(self, request, *args, **kwargs):
        device = self.get_object()
        return Response(device.config)

