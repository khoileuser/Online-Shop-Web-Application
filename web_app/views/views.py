from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


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
    from web_app.models import User
    print(User.objects.all().values())
    # User.objects.get(id=2).delete()
    return HttpResponse('ok')
