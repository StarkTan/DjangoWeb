from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import SnippetViewSet, UserViewSet, api_root
from rest_framework import renderers
from . import views
from rest_framework.routers import DefaultRouter
from django.urls import path, include



# 使用View后替换
# urlpatterns = [
#     # path('snippets/', views.snippet_list),
#     # path('snippets/<int:pk>/', views.snippet_detail),
#     path('', views.api_root),
#     path('snippets/', views.SnippetList.as_view(),name='snippet-list'),
#     path('snippets/<int:pk>/', views.SnippetDetail.as_view(),name='snippet-detail'),
#     path('users/', views.UserList.as_view(),name='user-list'),
#     path('users/<int:pk>/', views.UserDetail.as_view(),name='user-detail'),
#     path('snippets/<int:pk>/highlight/', views.SnippetHighlight.as_view(),name='snippet-highlight'),
#

# 使用路由后全部替换
# snippet_list = SnippetViewSet.as_view({
#             'get': 'list',
#             'post': 'create'
#         })
# snippet_detail = SnippetViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy'
# })
# snippet_highlight = SnippetViewSet.as_view({
#     'get': 'highlight'
# }, renderer_classes=[renderers.StaticHTMLRenderer])
# user_list = UserViewSet.as_view({
#     'get': 'list'
# })
# user_detail = UserViewSet.as_view({
#     'get': 'retrieve'
# })
#
# urlpatterns = [
#     path('', views.api_root),
#     path('snippets/', snippet_list,name='snippet-list'),
#     path('snippets/<int:pk>/',snippet_detail,name='snippet-detail'),
#     path('users/', user_list,name='user-list'),
#     path('users/<int:pk>/', user_detail,name='user-detail'),
#     path('snippets/<int:pk>/highlight/',snippet_highlight,name='snippet-highlight'),
# ]


# 因为使用的ViewSet不同于Django的View 修改了分发方式 所以使用router作为分发处理
router = DefaultRouter()

# register(self, prefix, viewset, basename=None)  如果ViewSet里面没有basename则需要填入basename参数
router.register(r'snippets', views.SnippetViewSet)
router.register(r'users', views.UserViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
# urlpatterns = format_suffix_patterns(urlpatterns)  # 返回一个 URL pattern 列表，其中包含附加到每个 URL pattern 的格式后缀模式

