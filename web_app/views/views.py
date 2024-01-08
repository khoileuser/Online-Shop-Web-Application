from django.http import HttpResponse
from django.template import loader

from web_app.models import Product


def index(request):
    if request.user != "guest":
        context = {
            "username": request.user.username,
            "cart_quantity": request.user.cart_quantity,
            "type": request.user.account_type
        }
    else:
        context = {
            "username": None,
            "cart_quantity": None,
            "type": None
        }

    products = Product.objects.all().order_by('?')[:18]
    context['trending1'] = list(products.values())[:3]
    context['trending2'] = list(products.values())[3:6]
    context['trending3'] = list(products.values())[6:9]
    context['new_arrival1'] = list(products.values())[9:12]
    context['new_arrival2'] = list(products.values())[12:15]
    context['new_arrival3'] = list(products.values())[15:18]

    template = loader.get_template("common/index.html")
    return HttpResponse(template.render(context, request))


def about(request):
    if request.user != "guest":
        context = {
            "username": request.user.username,
            "cart_quantity": request.user.cart_quantity,
            "type": request.user.account_type
        }
    else:
        context = {
            "username": None,
            "cart_quantity": None,
            "type": None
        }

    template = loader.get_template("common/about.html")
    return HttpResponse(template.render(context, request))


def terms(request):
    if request.user != "guest":
        context = {
            "username": request.user.username,
            "cart_quantity": request.user.cart_quantity,
            "type": request.user.account_type
        }
    else:
        context = {
            "username": None,
            "cart_quantity": None,
            "type": None
        }

    template = loader.get_template("common/terms.html")
    return HttpResponse(template.render(context, request))


def privacy(request):
    if request.user != "guest":
        context = {
            "username": request.user.username,
            "cart_quantity": request.user.cart_quantity,
            "type": request.user.account_type
        }
    else:
        context = {
            "username": None,
            "cart_quantity": None,
            "type": None
        }

    template = loader.get_template("common/privacy.html")
    return HttpResponse(template.render(context, request))


def execute(request):
    return HttpResponse("execute")
