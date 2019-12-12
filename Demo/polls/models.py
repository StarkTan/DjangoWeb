import datetime

from django.db import models
from django.utils import timezone


# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)  # 字符字段
    pub_date = models.DateTimeField('date published')  # 时间字段

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # 级联关系配置，多对一，级联删除
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)  # 数字字段

    def __str__(self):
        return self.choice_text



