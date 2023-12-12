from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from web_app.models import Cart, User


def cart_(request):
    if request.method != "GET":
        return HttpResponse("Invalid method")
    elif request.user == "guest":
        return redirect("/signin")

    template = loader.get_template("cart.html")
    context = {
        "username": request.user.username,
        "cart_quantity": request.user.cart_quantity,
        "products": Cart.objects().get(owner=request.user).products
    }
    return HttpResponse(template.render(context, request))


def add_to_cart(request):
    if request.method != "POST":
        return HttpResponse("Invalid method")
    elif request.user == "guest":
        return redirect("/signin")

    cart = Cart.objects.filter(owner=request.user).first()
    print(cart)
