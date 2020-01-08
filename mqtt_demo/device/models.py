from django.db import models

# Create your models here.


class Device(models.Model):

    id = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=200, blank=False)
    config = models.CharField(max_length=200, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    confirm = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)
