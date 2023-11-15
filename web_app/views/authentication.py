from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from web_app.models import User
from django.contrib.auth.hashers import make_password, check_password


def return_session(request, user):
    request.session["user_id"] = user.id
    request.session["name"] = user.name
    request.session["username"] = user.username
    request.session["cart_quantity"] = user.cart_quantity


@csrf_exempt
def sign_in(request):
    if request.method == "GET":
        template = loader.get_template('authentication/sign-in.html')
        return HttpResponse(template.render())
    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = User.objects.get(username=username)
        if check_password(password, user.password):
            return_session(request, user)
            return redirect("/")
        else:
            return HttpResponse("Invalid credentials")


@csrf_exempt
def sign_up(request):
    if request.method == "GET":
        template = loader.get_template('authentication/sign-up.html')
        return HttpResponse(template.render())
    elif request.method == "POST":
        name = request.POST["name"]
        username = request.POST["username"]
        password = request.POST["password"]
        hashed_pwd = make_password(password)
        account_type = "V" if request.POST["accounttype"] == "vendor" else "C"
        user = User(name=name, username=username,
                    password=hashed_pwd, account_type=account_type)
        user.save()
        return_session(request, user)
        return redirect("/")


def sign_out(request):
    fields = ["user_id", "name", "username", "cart_quantity"]
    for field in fields:
        try:
            del request.session[field]
        except KeyError:
            continue
    # return HttpResponse("You're logged out.")
    return redirect("/")
