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
        if re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,255}$', password) is None:
            return HttpResponse("Passwords must contain at least one uppercase, one lowercase, one digit, one special character and at least 8 characters long.")
        hashed_pwd = make_password(password)

        account_type = "V" if request.POST["accounttype"] == "vendor" else "C"

        try:
            user = User(name=name, username=username, password=hashed_pwd,
                        account_type=account_type, avatar=None)
        except:
            return HttpResponse("Invalid credentials")
        user.save()
        Cart(owner=user).save

        return_session(request, user)
        return redirect("/")


@csrf_exempt
def check_sign_up(request):
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
    return token_urlsafe(32)


def return_session(request, user):
    request.session["user_id"] = user.id
    generated_token = token_generator()
    request.session["token"] = generated_token
    if user.tokens is None:
        user.tokens = [generated_token]
    else:
        user.tokens.append(generated_token)
    user.save()


def sign_out(request):
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
