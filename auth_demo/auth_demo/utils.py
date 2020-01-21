from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse


def only_superuser(f):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user is None:
            return HttpResponseRedirect(reverse('login'))
        if not user.is_superuser:
            return HttpResponse("<p>Forbidden!!!!<p><br/><a href='/logout/'>退出</a>")
        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap
