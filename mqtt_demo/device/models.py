from django.db import models
import json
# Create your models here.


class Device(models.Model):

    id = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=200, blank=False)
    version = models.CharField(max_length=20, blank=False)
    config = models.CharField(max_length=200, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    confirm = models.BooleanField(default=True)

    def pub_msg(self):
        res = {'sn': self.id,
               'name': self.name,
               'version': self.version,
               'config': json.loads(self.config)}
        return res


    class Meta:
        ordering = ('created',)
