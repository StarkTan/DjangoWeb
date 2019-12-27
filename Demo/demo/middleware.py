from django.utils.deprecation import MiddlewareMixin


class My1MiddleWare(MiddlewareMixin):

    def __init__(self, get_response=None):
        self.get_response = get_response

    def process_request(self, request):
        """
        可以对请求进行预处理，不需要返回，Djangoo会自动传递
        """
        print("MW1.process_request")

    def process_view(self, request, callback, callback_args, callback_kwargs):
        """
        可以使用 response=callback(request,*callback_args,**callback_kwargs) 进行视图处理
        返回 response 可以停止后续的 process_view
        """
        print("MW1.process_view")

    def process_template_response(self, request, response):
        """
        如果视图函数返回的对象要有一个 render() 方法（或者表明该对象是一个 TemplateResponse 对象或等价方法）时执行
        """
        print("MW1.process_template_response")
        return response

    def process_exception(self, request, exception):
        """
        函数只在视图函数中出现异常的时候才执行，它返回的值可以是 None，也可以是一个 HttpResponse 对象
        如果返回 None，则继续由下一个中间件的 process_exception 方法来处理异常
        如果返回 HttpResponse，将调用中间件中的 process_response 方法
        """
        print("MW1.process_exception")

    def process_response(self, request, response):
        """
        在请求返回时候可以进行的处理
        """
        print("MW1.process_response")
        return response


class My2MiddleWare(MiddlewareMixin):

    def process_request(self, request):
        print("MW2.process_request")

    def process_view(self, request, callback, callback_args, callback_kwargs):
        print("MW2.process_view")

    def process_template_response(self, request, response):
        print("MW2.process_template_response")
        return response

    def process_exception(self, request, exception):
        print("MW2.process_exception")

    def process_response(self, request, response):
        print("MW2.process_response")
        return response
