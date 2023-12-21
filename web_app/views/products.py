from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from web_app.models import Product


def listing(request):
    template = loader.get_template("products/listing.html")
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
    return HttpResponse(template.render(context, request))


def product(request, product_id):
    template = loader.get_template("products/product.html")
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
    product = Product.objects.get(id=product_id)
    context["product_id"] = product.id
    context["category"] = product.category
    context["name"] = product.name
    context["price"] = product.price
    context["description"] = product.description
    context["images"] = product.images
    return HttpResponse(template.render(context, request))
