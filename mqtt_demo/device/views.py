from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Device
from .serializers import DeviceSerializer
# Create your views here.
from rest_framework import viewsets, mixins


class DeviceViewSet(mixins.UpdateModelMixin,
                     viewsets.ReadOnlyModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    @action(methods=['GET'],detail=True)
    def config(self, request, *args, **kwargs):
        device = self.get_object()
        return Response(device.config)

