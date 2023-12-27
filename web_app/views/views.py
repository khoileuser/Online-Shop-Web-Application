from django.shortcuts import render
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
    context['trending2'] = list(products.values())[3:7]
    context['trending3'] = list(products.values())[7:10]
    context['new_arrival1'] = list(products.values())[10:14]
    context['new_arrival2'] = list(products.values())[14:18]
    context['new_arrival3'] = list(products.values())[18:22]

    template = loader.get_template("index.html")
    return HttpResponse(template.render(context, request))


def execute(request):
    from web_app.models import Order, Cart, CartProduct
    cart = Cart.objects.all().values()
    print(cart)
    order = Order.objects.all().values()
    print(order)
    cart_product = CartProduct.objects.all().values()
    print(cart_product)
    return HttpResponse('ok')
