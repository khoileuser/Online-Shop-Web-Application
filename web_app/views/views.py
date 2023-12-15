from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.hashers import make_password


def index(request):
    template = loader.get_template("index.html")
    if request.user != "guest":
        context = {
            "username": request.user.username,
            "cart_quantity": request.user.cart_quantity
        }
    else:
        context = {
            "username": None,
            "cart_quantity": None
        }
    return HttpResponse(template.render(context, request))


def execute(request):
    from web_app.models import Product, User
    # print(Product.objects.all().values())
    print(User.objects.all().values())
    # User.objects.get(id=1).delete()
    return HttpResponse('ok')
