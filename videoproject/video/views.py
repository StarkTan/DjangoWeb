from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views import generic
from django.views.decorators.http import require_http_methods

from helpers import get_page_list, ajax_required # 不用处理，django能找到

from .models import Video, Classification
from .forms import CommentForm

class IndexView(generic.ListView):
    model = Video  # 作用于Video模型
    template_name = 'video/index.html'
    context_object_name = 'video_list'
    paginate_by = 12  # 分页功能，每页展示12条
    c = None

    # 传入额外的数据
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        page_list = get_page_list(paginator, page)
        classification_list = Classification.objects.filter(status=True).values()
        context['c'] = self.c
        context['classification_list'] = classification_list
        context['page_list'] = page_list
        return context

    # 增加过滤排序功能
    def get_queryset(self):
        self.c = self.request.GET.get("c", None)
        if self.c:
            classification = get_object_or_404(Classification, pk=self.c)
            return classification.video_set.all().order_by('-create_time')
        else:
            return Video.objects.filter(status=0).order_by('-create_time')


class SearchListView(generic.ListView):
    model = Video
    template_name = 'video/search.html'
    context_object_name = 'video_list'
    paginate_by = 8
    q = ''

    def get_queryset(self):
        self.q = self.request.GET.get("q","")
        return Video.objects.filter(title__contains=self.q).filter(status=0)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SearchListView, self).get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        page_list = get_page_list(paginator, page)
        context['page_list'] = page_list
        context['q'] = self.q
        return context


class VideoDetailView(generic.DetailView):
    model = Video
    template_name = 'video/detail.html'

    # 每次调用DetailView的时候，django都会回调get_object()这个函数
    def get_object(self, queryset=None):
        obj = super().get_object()
        obj.increase_view_count()  # 调用自增函数
        return obj

    def get_context_data(self, **kwargs):
        context = super(VideoDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        context['form'] = form
        return context


# 用ajax_required 和 @require_http_methods(["POST"]) 分别验证request必须是ajax和post请求
@ajax_required
@require_http_methods(["POST"])
def like(request):
    if not request.user.is_authenticated:
        return JsonResponse({"code": 1, "msg": "请先登录"})
    video_id = request.POST['video_id']
    video = Video.objects.get(pk=video_id)
    user = request.user
    video.switch_like(user)
    return JsonResponse({"code": 0, "likes": video.count_likers(), "user_liked": video.user_liked(user)})

@ajax_required
@require_http_methods(["POST"])
def collect(request):
    if not request.user.is_authenticated:
        return JsonResponse({"code": 1, "msg": "请先登录"})
    video_id = request.POST['video_id']
    video = Video.objects.get(pk=video_id)
    user = request.user
    video.switch_collect(user)
    return JsonResponse({"code": 0, "collects": video.count_collecters(), "user_collected": video.user_collected(user)})