from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def test(request):
    print(request)
    if request.method == 'GET':
        print(request.GET)
    if request.method == 'POST':
        print(request.GET)
        print(request.POST)
        print(request.body)
    return JsonResponse({'code':200})
