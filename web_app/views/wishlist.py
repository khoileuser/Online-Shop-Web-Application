from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

from web_app.models import User, Product


def view_wishlist(request, username):
    """
    The `view_wishlist` function retrieves and organizes a user's wishlist products by vendor and
    renders them in a template.

    :param request: The request parameter is an object that represents the HTTP request made by the
    user. It contains information such as the request method (GET, POST, etc.), headers, and user
    session data
    :param username: The username parameter is the username of the user whose wishlist is being viewed
    :return: an HttpResponse object.
    """
    if request.method != "GET":
        return HttpResponse("Invalid method")

    context = {}

    try:
        if username == request.user.username:
            user = request.user
            context = {
                "username": user.username,
                "cart_quantity": user.cart_quantity,
                "type": user.account_type,
                "is_owner": True,
                "owner_name": user.name,
                "share": user.share_wishlist
            }
    except:
        user = User.objects.get(username=username)
        if user.share_wishlist == False:
            return HttpResponse("This wishlist is not being shared")
        context = {
            "username": None,
            "cart_quantity": None,
            "type": None,
            "is_owner": False,
            "owner_name": user.name
        }

    wishlist = user.wishlist.all().order_by('id')

    # append all vendor exist in user's cart
    vendors = []
    [vendors.append(wishlist_product.owner)
     for wishlist_product in wishlist if wishlist_product.owner not in vendors]

    # group vendor
    products_by_vendor = []
    for vendor in vendors:
        # group products by vendor
        _wishlist_products = [
            wishlist_product for wishlist_product in wishlist if wishlist_product.owner == vendor]
        products_by_vendor.append({
            "vendor": {
                "id": vendor.id,
                "name": vendor.name,
                "username": vendor.username
            },
            "cart_products": _wishlist_products,
        })

    context["products_by_vendor"] = products_by_vendor

    template = loader.get_template('me/wishlist.html')
    return HttpResponse(template.render(context, request))


@csrf_exempt
def add_to_wishlist(request, product_id):
    """
    The function adds a product to the user's wishlist if the user is a customer and the request method
    is POST.

    :param request: The `request` parameter is an object that represents the HTTP request made by the
    user. It contains information such as the method used (GET, POST, etc.), user session data, and any
    data sent in the request
    :param product_id: The product_id parameter is the unique identifier of the product that the user
    wants to add to their wishlist
    :return: a redirect to the previous page (HTTP_REFERER) after adding a product to the user's
    wishlist.
    """
    if request.method != "POST":
        return HttpResponse("Invalid method")
    elif request.user == "guest":
        return redirect("/signin")
    elif request.user.account_type != "C":
        return HttpResponse('You are not a customer')

    product = Product.objects.get(id=product_id)
    if not request.user.wishlist.filter(id=product.id).exists():
        request.user.wishlist.add(product)
        request.user.save()

    return redirect(request.META['HTTP_REFERER'])


@csrf_exempt
def remove_from_wishlist(request, product_id):
    """
    The function removes a product from a user's wishlist if the user is a customer and the request
    method is POST.

    :param request: The `request` parameter is an object that represents the HTTP request made by the
    client. It contains information such as the method used (GET, POST, etc.), user information, and any
    data sent with the request
    :param product_id: The product_id parameter is the unique identifier of the product that the user
    wants to remove from their wishlist
    :return: a redirect to the previous page (the page specified in the 'HTTP_REFERER' header of the
    request).
    """
    if request.method != "POST":
        return HttpResponse("Invalid method")
    elif request.user == "guest":
        return redirect("/signin")
    elif request.user.account_type != "C":
        return HttpResponse('You are not a customer')

    product = Product.objects.get(id=product_id)
    try:
        request.user.wishlist.remove(product)
        request.user.save()
    except:
        pass

    return redirect(request.META['HTTP_REFERER'])


@csrf_exempt
def share_toggle(request, value):
    """
    The function `share_toggle` updates the `share_wishlist` attribute of the user based on the value
    provided and redirects the user to the previous page.

    :param request: The `request` parameter is an object that represents the HTTP request made by the
    client. It contains information about the request, such as the user making the request, the HTTP
    method used (e.g., GET, POST), and any data sent with the request
    :param value: The "value" parameter is a string that represents whether the user wants to toggle the
    sharing of their wishlist. It can have two possible values: "true" or "false"
    :return: a redirect to the previous page.
    """
    if value == "true":
        request.user.share_wishlist = True
    elif value == "false":
        request.user.share_wishlist = False
    request.user.save()

    return redirect(request.META['HTTP_REFERER'])
