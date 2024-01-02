from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

from web_app.models import Cart, Product


def view_cart(request):
    """
    The `view_cart` function retrieves the user's cart, groups the products by vendor, calculates the
    total price of the cart, and renders the cart template with the necessary context.

    :param request: The `request` parameter is an object that represents the HTTP request made by the
    user. It contains information such as the request method (GET, POST, etc.), user information, and
    any data sent with the request
    :return: an HttpResponse object.
    """
    if request.method != "GET":
        return HttpResponse("Invalid method")
    elif request.user == "guest":
        return redirect("/signin")
    elif request.user.account_type != "C":
        return HttpResponse('You are not a customer')

    # get user's cart
    try:
        cart = Cart.objects.get(owner=request.user)
    except:
        cart = Cart.objects.create(owner=request.user)

    cart_products = cart.products.all().order_by('id')

    # append all vendor exist in user's cart
    vendors = []
    [vendors.append(cart_product.product.owner)
     for cart_product in cart_products if cart_product.product.owner not in vendors]

    # group vendor
    products_by_vendor = []
    for vendor in vendors:
        # group products by vendor
        _cart_products = [
            cart_product for cart_product in cart_products if cart_product.product.owner == vendor]
        products_by_vendor.append({
            'vendor': {
                "id": vendor.id,
                "name": vendor.name,
                "username": vendor.username
            },
            'cart_products': _cart_products,
        })

    # calculate total price of user's cart
    total_price = 0
    for cart_product in cart_products:
        total_price = total_price + \
            (cart_product.product.price * cart_product.quantity)

    template = loader.get_template("cart.html")
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
    """
    The function adds a product to the user's cart with the specified quantity, and updates the user's
    cart quantity.

    :param request: The request parameter is an object that represents the HTTP request made by the
    client. It contains information such as the method used (GET, POST, etc.), user information, and any
    data sent with the request
    :param product_id: The product_id parameter is the unique identifier of the product that the user
    wants to add to their cart
    :param quantity: The quantity parameter represents the number of units of the product that the user
    wants to add to their cart
    :return: an HttpResponse object with a status code of 200.
    """
    if request.method != "POST":
        return HttpResponse("Invalid method")
    elif request.user == "guest":
        return redirect("/signin")
    elif request.user.account_type != "C":
        return HttpResponse('You are not a customer')

    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(owner=request.user)
    except:
        cart = Cart.objects.create(owner=request.user)
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
        user = request.user
        user.cart_quantity += 1
        user.save()
    return HttpResponse(200)


def del_product(product, user):
    """
    The function deletes a product and updates the user's cart quantity.

    :param product: The product parameter is an instance of a product object that needs to be deleted
    from the database
    :param user: The user parameter represents the user object whose cart is being modified
    """
    product.delete()
    user.cart_quantity -= 1
    if user.cart_quantity <= 0:
        user.cart_quantity = 0
    user.save()


@csrf_exempt
def remove_from_cart(request, product_id, quantity):
    """
    The function removes a specified quantity of a product from the user's cart, or removes the product
    entirely if the quantity is set to 'all'.

    :param request: The `request` parameter is an object that represents the HTTP request made by the
    client. It contains information such as the request method, user, and other data related to the
    request
    :param product_id: The product_id parameter is the unique identifier of the product that needs to be
    removed from the cart
    :param quantity: The "quantity" parameter represents the number of products to be removed from the
    cart. It can be an integer value or the string 'all'. If the value is 'all', it means that all the
    products of that particular type will be removed from the cart
    :return: an HttpResponse with a status code of 200.
    """
    if request.method != "POST":
        return HttpResponse("Invalid method")
    elif request.user == "guest":
        return redirect("/signin")
    elif request.user.account_type != "C":
        return HttpResponse('You are not a customer')

    cart = Cart.objects.get(owner=request.user)
    exist = None
    try:
        exist = cart.products.all().get(product_id=product_id)
    except:
        pass
    if exist:
        if quantity == 'all':
            del_product(exist, request.user)
        else:
            quantity = int(quantity)
            exist.quantity -= quantity
            if exist.quantity <= 0:
                del_product(exist, request.user)
            else:
                exist.save()
    return HttpResponse(200)
