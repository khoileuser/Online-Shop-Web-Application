from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


def index(request):
    template = loader.get_template("index.html")
    context = {
        "user_id": request.session.get("user_id"),
        "name": request.session.get("name"),
        "username": request.session.get("username"),
        "cart_quantity": request.session.get("cart_quantity")
    }
    return HttpResponse(template.render(context, request))


def execute(request):
    print('1')
    from web_app.models import User
    print('2')
    print(User.objects.all().values())
    return HttpResponse('ok')
