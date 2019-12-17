from django.db import models


# Create your models here.
class Classification(models.Model):
    list_display = ("title",)
    title = models.CharField(max_length=100, blank=True, null=True)  # 分类名称
    status = models.BooleanField(default=True)  # 是否启用

    class Meta:
        db_table = "v_classification"


class Video(models.Model):
    STATUS_CHOICES = (
        ('0', '发布中'),
        ('1', '未发布'),
    )
    title = models.CharField(max_length=100,blank=True, null=True)  # 视频标题
    desc = models.CharField(max_length=255,blank=True, null=True)  # 视频描述
    classification = models.ForeignKey(Classification, on_delete=models.CASCADE, null=True)  # 视频分类
    file = models.FileField(max_length=255)  # 视频文件地址
    cover = models.ImageField(upload_to='cover/', blank=True, null=True)  # 视频封面。数据类型是ImageField
    status = models.CharField(max_length=1 ,choices=STATUS_CHOICES, blank=True, null=True)  # 视频状态
    create_time = models.DateTimeField(auto_now_add=True, blank=True, max_length=20)
