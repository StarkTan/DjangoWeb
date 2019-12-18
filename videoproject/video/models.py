from django.db import models


# Create your models here.
from django.conf import settings


class Classification(models.Model):
    list_display = ("title",)
    title = models.CharField(max_length=100, blank=True, null=True)  # 分类名称
    status = models.BooleanField(default=True)  # 是否启用

    class Meta:
        db_table = "v_classification"


class VideoQuerySet(models.query.QuerySet):
    def get_recommend_list(self):
        return self.filter(status=0).order_by('-view_count')[:4]

    def get_search_list(self, q):
        if q:
            return self.filter(title__contains=q).order_by('-create_time')
        else:
            return self.order_by('-create_time')


class Video(models.Model):
    objects = VideoQuerySet.as_manager()  # 表示用VideoQuerySet作为Video的查询管理器
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
    view_count = models.IntegerField(default=0, blank=True)  # 观看次数
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL,  # 喜欢的用户
                                   blank=True, related_name="liked_videos")
    collected = models.ManyToManyField(settings.AUTH_USER_MODEL, # 收藏的用户
                                       blank=True, related_name="collected_videos")
    create_time = models.DateTimeField(auto_now_add=True, blank=True, max_length=20)

    def increase_view_count(self):
        self.view_count += 1
        self.save(update_fields=['view_count'])

    def switch_like(self, user):
        if user in self.liked.all():
            self.liked.remove(user)
        else:
            self.liked.add(user)

