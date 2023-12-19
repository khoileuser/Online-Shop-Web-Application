from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from web_app.models import Cart, User, Product
from django.views.decorators.csrf import csrf_exempt


def view_cart(request):
    if request.method != "GET":
        return HttpResponse("Invalid method")
    elif request.user == "guest":
        return redirect("/signin")

    template = loader.get_template("cart.html")
    context = {
        "username": request.user.username,
        "cart_quantity": request.user.cart_quantity,
        "type": request.user.account_type,
        "products": Cart.objects().get(owner=request.user).products
    }
    return HttpResponse(template.render(context, request))


@csrf_exempt
def add_to_cart(request, product_id, quantity):
    if request.method != "POST":
        return HttpResponse("Invalid method")
    elif request.user == "guest":
        return redirect("/signin")

    cart = Cart.objects.get(owner=request.user)
    cart.products.append({
        'product': Product.objects.get(id=product_id),
        'quantity': int(quantity)
    })
    cart.save()
    return HttpResponse(200)
