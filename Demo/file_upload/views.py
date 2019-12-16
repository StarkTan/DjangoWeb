import os

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

folder_path = os.path.join(os.getcwd(), r'file_upload\static\file_upload\upload')


# Create your views here.
def index(request):
    files = os.listdir(folder_path)
    return render(request, 'file_upload/index.html', {'files': files})


def file_upload(request):
    obj = request.FILES.get('file')
    if obj is None:
        return HttpResponseRedirect(reverse('file_upload:index'))
    path = os.path.join(folder_path, obj.name)
    f = open(path, 'wb')
    for chunk in obj.chunks():
        f.write(chunk)
    f.close()
    return HttpResponseRedirect(reverse('file_upload:index'))


def file_delete(request):
    name = request.GET.get("name")
    path = os.path.join(folder_path, name)
    if os.path.exists(path):
        os.remove(path)
        return HttpResponseRedirect(reverse('file_upload:index'))
    else:
        return Http404()
