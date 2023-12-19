from web_app.models import User
from secrets import compare_digest
from django.http import HttpResponse


class Authentication:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # if request.method == "POST":
        #     response = self.get_response(request)
        #     return response

        try:
            user_id = request.session.get("user_id")
            if user_id:
                user = User.objects.get(id=user_id)
            else:
                request.user = "guest"
                response = self.get_response(request)
                return response

            request_token = request.session.get("token")
            tokens = user.tokens
            for token in tokens:
                if compare_digest(token, request_token):
                    request.user = user
                    response = self.get_response(request)
                    return response

            return HttpResponse("Invalid credentials")
        except Exception as e:
            fields = ["user_id", "token"]
            for field in fields:
                try:
                    del request.session[field]
                except KeyError:
                    continue
            return HttpResponse("Authetications failed, cleaned stored credentials")

    def process_exception(self, request, exception):
        pass

    def process_template_response(self, request, response):
        pass
