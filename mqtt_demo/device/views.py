from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Device
from .serializers import DeviceSerializer
# Create your views here.
from rest_framework import viewsets, mixins
from mqtt_client.mqtt_config import client

pub_pre = '/usi/cloud/config/'

class DeviceViewSet(mixins.UpdateModelMixin,
                     viewsets.ReadOnlyModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.validated_data['confirm'] = False
        serializer.save()
        sn = serializer.data['id']
        config = serializer.data['config']
        # 推送数据
        client.publish(pub_pre + sn, config, qos=1)

    @action(methods=['GET'],detail=True)
    def config(self, request, *args, **kwargs):
        device = self.get_object()
        return Response(device.config)

