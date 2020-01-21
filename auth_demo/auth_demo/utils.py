from django.contrib.sessions.models import Session
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.utils import timezone


def only_superuser(f):
    def wrap(request, *args, **kwargs):
        user = request.user
        if not user.is_superuser:
            return HttpResponse("<p>Forbidden!!!!<p><br/><a href='/logout/'>退出</a>")
        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


def single_session(request):
    # 登录之后获取获取最新的session_key
    session_key = request.session.session_key
    print(session_key)
    print(Session.objects.filter(~Q(session_key=session_key), expire_date__gte=timezone.now()))
    # 删除非当前用户session_key的记录
    for session in Session.objects.filter(~Q(session_key=session_key), expire_date__gte=timezone.now()):
        data = session.get_decoded()
        if data.get('_auth_user_id', None) == str(request.user.id):
            session.delete()





