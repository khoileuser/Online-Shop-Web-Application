from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from web_app.models import Product

import random


def index(request):
    template = loader.get_template("index.html")
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
    context['trending2'] = list(products.values())[3:7]
    context['trending3'] = list(products.values())[7:10]
    context['new_arrival1'] = list(products.values())[10:14]
    context['new_arrival2'] = list(products.values())[14:18]
    context['new_arrival3'] = list(products.values())[18:22]
    return HttpResponse(template.render(context, request))


def execute(request):
    from web_app.models import Product, User, Cart
    user = User.objects.get(name="Test Customer 1")
    print(user)
    cart = Cart.objects.all().values()
    print(cart)
    # Cart.objects.get(id=9).delete()
    # cart = Cart(owner=user, total_price=0)
    # cart.save()
    return HttpResponse('ok')
