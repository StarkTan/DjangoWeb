from rest_framework import serializers
from .models import Device


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('id', 'name', 'config', 'version', 'confirm')
        read_only_fields = ("id", 'name', 'confirm', 'version')
