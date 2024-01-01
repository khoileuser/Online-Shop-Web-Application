from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from web_app.models import User, Cart
from django.contrib.auth.hashers import make_password, check_password
from secrets import token_urlsafe

import re


@csrf_exempt
def sign_in(request):
    """
    The `sign_in` function handles the logic for user sign-in, checking if the user exists in the
    database and verifying their credentials.

    :param request: The `request` parameter is an object that represents the HTTP request made by the
    client. It contains information such as the request method (GET, POST, etc.), headers, user session,
    and any data sent with the request
    :return: The code is returning an HttpResponse object.
    """
    if request.method == "GET":
        if request.user == "guest":
            template = loader.get_template('authentication/sign-in.html')
            return HttpResponse(template.render())
        else:
            return redirect("/")
    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        try:
            user = User.objects.get(username=username)
            if check_password(password, user.password):
                return_session(request, user)
                return redirect("/")
            else:
                return HttpResponse("Invalid credentials")
        except:
            return HttpResponse("Cannot find this user in the database, have you signed?")


@csrf_exempt
def check_sign_in(request):
    """
    The function checks if a user's sign-in credentials are valid and returns "true" if they are, and
    "false" if they are not.

    :param request: The `request` parameter is an object that represents the HTTP request made by the
    client. It contains information such as the request method (e.g., GET, POST), headers, cookies, and
    the request body
    :return: an HttpResponse object. The content of the HttpResponse object depends on the conditions
    met in the code. If the username and password are correct, it returns "true". If the username or
    password is incorrect, it returns "false".
    """
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        try:
            user = User.objects.get(username=username)
            if check_password(password, user.password):
                return_session(request, user)
                return HttpResponse("true")
            else:
                return HttpResponse("false")
        except:
            return HttpResponse("false")


@csrf_exempt
def sign_up(request):
    """
    The `sign_up` function handles the sign-up process for a user, validating their input and creating a
    new user account if the input is valid.

    :param request: The `request` parameter is an object that represents the HTTP request made by the
    client. It contains information such as the request method (GET or POST), the user making the
    request, and any data sent with the request (e.g., form data)
    :return: an HTTP response.
    """
    if request.method == "GET":
        if request.user == "guest":
            template = loader.get_template('authentication/sign-up.html')
            return HttpResponse(template.render())
        else:
            return redirect("/")
    elif request.method == "POST":
        name = request.POST["name"]
        if len(name) > 255 or len(name) == 0:
            return HttpResponse("Name must be lower than 255 characters and not empty.")

        username = request.POST["username"]
        if len(username) < 4 or len(username) > 25 or re.match(r'^[a-zA-Z0-9]+$', username) is None:
            return HttpResponse("Usernames must contain only letters and digits and between 4 and 25 characters.")

        password = request.POST["password"]
        if re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,4096}$', password) is None:
            return HttpResponse("Passwords must contain at least one uppercase, one lowercase, one digit, one special character and at least 8 characters long.")
        hashed_pwd = make_password(password)

        account_type = "V" if request.POST["accounttype"] == "vendor" else "C"

        try:
            user = User(name=name, username=username, password=hashed_pwd,
                        account_type=account_type, avatar=None)
        except:
            return HttpResponse("Invalid credentials")
        user.save()

        Cart.objects.create(owner=user)

        return_session(request, user)
        return redirect("/")


@csrf_exempt
def check_sign_up(request):
    """
    The function checks if a username already exists in the User model and returns "true" if it does,
    and "false" if it doesn't.

    :param request: The `request` parameter is an object that represents the HTTP request made by the
    client. It contains information such as the request method (e.g., GET or POST), the request headers,
    and the request data
    :return: an HttpResponse object. The content of the HttpResponse object depends on the conditions in
    the code. If a user with the given username already exists, it will return "true". If a user with
    the given username does not exist, it will return "false". If there is an exception during the
    process, it will also return "false".
    """
    if request.method == "POST":
        username = request.POST["username"]
        try:
            user = User.objects.get(username=username)
            if user:
                return HttpResponse("true")
            else:
                return HttpResponse("false")
        except:
            return HttpResponse("false")


def token_generator():
    """
    The function `token_generator` generates a random URL-safe token of length 32.
    :return: a randomly generated token of length 32.
    """
    return token_urlsafe(32)


def return_session(request, user):
    """
    The function sets the user ID and generates a token for the user's session, and then adds the token
    to the user's list of tokens.

    :param request: The "request" parameter is an object that represents the HTTP request made by the
    client. It contains information about the request, such as the headers, body, and session data
    :param user: The "user" parameter is an instance of a user model. It represents the user for whom
    the session is being created or updated
    """
    request.session["user_id"] = user.id
    generated_token = token_generator()
    request.session["token"] = generated_token
    if user.tokens is None:
        user.tokens = [generated_token]
    else:
        user.tokens.append(generated_token)
    user.save()


def sign_out(request):
    """
    The `sign_out` function removes the token associated with the user from the session and redirects
    the user to the homepage.

    :param request: The `request` parameter is an object that represents the HTTP request made by the
    user. It contains information about the request, such as the user making the request, the session
    data, and any data sent in the request body or query parameters
    :return: a redirect to the homepage ("/").
    """
    if request.user != 'guest':
        requested_token = request.session.get("token")
        request.user.tokens.remove(requested_token)
        request.user.save()

        fields = ["user_id", "token"]
        for field in fields:
            try:
                del request.session[field]
            except KeyError:
                continue
    return redirect("/")
