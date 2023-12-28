from web_app.models import User
from secrets import compare_digest
from django.http import HttpResponse


# The `Authentication` class is a middleware that handles user authentication by checking session
# credentials and comparing them with stored tokens.
class Authentication:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        The above function is a middleware in Python that handles user authentication by checking if the
        user's token matches any of the tokens stored in the user's tokens list.

        :param request: The `request` parameter is an object that represents an HTTP request made by a
        client to a server. It contains information such as the request method, headers, body, and session
        data
        :return: The code is returning an HttpResponse with the message "Invalid credentials" if the user's
        credentials are not valid. If an exception occurs during the authentication process, it returns an
        HttpResponse with the message "Authentication failed, cleaned stored credentials".
        """
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
