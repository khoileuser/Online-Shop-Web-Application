from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from web_app.models import Cart, User


def cart_(request):
    if request.user == "guest":
        template = loader.get_template("cart.html")
        return HttpResponse(template.render())
    else:
        return redirect("/signin")


def add_to_cart(request):
    if request.user == "guest":
        cart = Cart.objects.filter(owner=User.objects.get(
            id=request.session["user_id"])).first()
        print(cart)
    else:
        return redirect("/signin")
