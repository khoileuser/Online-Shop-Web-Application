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

    template = loader.get_template("cart/cart.html")

    # get user's cart
    cart = Cart.objects.get(owner=request.user)
    cart_products = cart.products.all()

    # append all vendor exist in user's cart
    vendors = []
    [vendors.append(cart_product.product.owner)
     for cart_product in cart_products if cart_product.product.owner not in vendors]

    # group vendor
    products_by_vendor = {}
    for vendor in vendors:
        # group products by vendor
        _cart_products = [
            cart_product for cart_product in cart_products if cart_product.product.owner == vendor]
        products_by_vendor[vendor.id] = {
            'vendor': vendor,
            'cart_products': _cart_products,
        }

    # calculate total price of user's cart
    total_price = 0
    for cart_product in cart_products:
        total_price = total_price + \
            (cart_product.product.price * cart_product.quantity)

    context = {
        "username": request.user.username,
        "cart_quantity": request.user.cart_quantity,
        "type": request.user.account_type,
        "products_by_vendor": products_by_vendor,
        "total_price": round(total_price, 2)
    }
    return HttpResponse(template.render(context, request))


@csrf_exempt
def add_to_cart(request, product_id, quantity):
    if request.method != "POST":
        return HttpResponse("Invalid method")
    elif request.user == "guest":
        return redirect("/signin")

    product = Product.objects.get(id=product_id)
    cart = Cart.objects.get(owner=request.user)
    exist = None
    try:
        exist = cart.products.all().get(product_id=product_id)
    except:
        pass
    if exist:
        exist.quantity += quantity
        exist.save()
    else:
        cart.products.create(product=product, quantity=quantity)
        user = User.objects.get(id=request.user.id)
        user.cart_quantity += 1
        user.save()
    return HttpResponse(200)


def del_product(product, user_id):
    product.delete()
    user = User.objects.get(id=user_id)
    user.cart_quantity -= 1
    if user.cart_quantity <= 0:
        user.cart_quantity = 0
    user.save()


@csrf_exempt
def remove_from_cart(request, product_id, quantity):
    if request.method != "POST":
        return HttpResponse("Invalid method")
    elif request.user == "guest":
        return redirect("/signin")

    product = Product.objects.get(id=product_id)
    cart = Cart.objects.get(owner=request.user)
    exist = None
    try:
        exist = cart.products.all().get(product_id=product_id)
    except:
        pass
    if exist:
        if quantity == 'all':
            del_product(exist, request.user.id)
        else:
            quantity = int(quantity)
            exist.quantity -= quantity
            if exist.quantity <= 0:
                del_product(exist, request.user.id)
            else:
                exist.save()
    return HttpResponse(200)


def checkout(request):
    products_by_vendor = request.POST["products_by_vendor"]

    template = loader.get_template("cart/checkout.html")
    return HttpResponse(template.render())
