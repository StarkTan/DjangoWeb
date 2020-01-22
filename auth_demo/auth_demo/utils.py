import time

from django.contrib.sessions.models import Session
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
import jwt


def only_superuser(f):
    def wrap(request, *args, **kwargs):
        user_info = request.user_info
        if user_info is not None:
            if user_info['super_user'] is True:
                return f(request, *args, **kwargs)
            else:
                response = {"status": 403,
                            "message": "Permission Deny!"}
                return JsonResponse(response)
        else:
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


secret = b'djaongo_jwt'
algorithm = 'HS256'
expire_time = 24*60*60


def get_token(obj):
    encoded = jwt.encode(obj, secret, algorithm='HS256')
    token = str(encoded, encoding='ascii')
    return token


def get_user_info(token):
    user_info = jwt.decode(token, secret, algorithm='HS256')
    return user_info


def token_auth(f):
    def wrap(request, *args, **kwargs):
        token = request.GET.get('token')
        if token is None:
            token = request.META.get("HTTP_TOKEN")
        if token is None:
            response = {"status": 403,
                        "message": "No  Authentication!"}  # Permission Deny!
            return JsonResponse(response)
        try:
            user_info = get_user_info(token)
            timestamp = user_info['timestamp']
            if time.time() > expire_time+timestamp:
                response = {"status": 403,
                            "message": "Authentication Out Of Time!"}  # Permission Deny!
                return JsonResponse(response)
            else:
                request.user_info = user_info
        except Exception:
            response = {"status": 403,
                        "message": "Authentication Failed!"}  # Permission Deny!
            return JsonResponse(response)
        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap

