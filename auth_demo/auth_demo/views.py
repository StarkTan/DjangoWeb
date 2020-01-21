from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .utils import only_superuser


def my_login(request):
    # 如果是GET方法，渲染到登录页面，如果是POST方法，进行登录判断
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        telephone = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')
        # 验证账号密码是否正确
        user = authenticate(request, username=telephone, password=password)
        if user is not None:
            # 判断用户是否被冰冻
            if user.is_active:
                login(request, user)
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


@only_superuser
def index(request):
    return HttpResponse("<p>Hello :"+request.user.username+"<p><br/><a href='/logout/'>退出</a>")

