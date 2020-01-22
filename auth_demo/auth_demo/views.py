from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .utils import only_superuser, single_session, get_token, token_auth
from django.contrib.auth.decorators import login_required
import time

def my_login(request):
    # 如果是GET方法，渲染到登录页面，如果是POST方法，进行登录判断
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')
        # 验证账号密码是否正确
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # 判断用户是否被冰冻
            if user.is_active:
                login(request, user)
                # 设置单一登录
                single_session(request)
                # 判断是否记住密码
                if remember:
                    request.session.set_expiry(24*60*60)
                else:
                    # 设置浏览器关闭之后就过期
                    request.session.set_expiry(0)
                    # 这里的设置网址有next后缀的处理方法
                    next_url = request.GET.get('next')
                    if next_url:
                        # 重定向到设置好的登录页面
                        return redirect(next_url)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("用户已冰冻！")
        else:
            return HttpResponse("用户名或密码错误！")


def my_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


@login_required(login_url="/login/")
@only_superuser
def index(request):
    return HttpResponse("<p>Hello :"+request.user.username+"<p><br/><a href='/logout/'>退出</a>")


@csrf_exempt
def auth(request):
    if not request.method == 'POST':
        response = {"status": 405,
                    "message": "method not allowed!"}
        return JsonResponse(response)
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            response = {'status': 401,
                       'message':  "username or password error!"}
            return JsonResponse(response)
        else:
            user_info = {"id": user.id,
                         "super_user": user.is_superuser,
                         "timestamp": time.time()}
            token = get_token(user_info)
            response = {'status': 200,
                        'usernam': user.username,
                        'token': token}
            return JsonResponse(response)


@csrf_exempt
@token_auth
@only_superuser
def users(request):
    if not request.method == 'GET':
        response = {"status": 405,
                    "message": "method not allowed!"}
        return JsonResponse(response)

    users = User.objects.all()
    data = []
    for user in users:
        user_info = {"id": user.id,
                     "username": user.username,
                     "email": user.email}
        data.append(user_info)
    response = {"status": 405,
                "data": data}
    return JsonResponse(response)


