from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from web_app.models import Cart, User, Product
from django.views.decorators.csrf import csrf_exempt


def get_cart_products(user):
    """
    The function `get_cart_products` retrieves all the products in a user's cart.

    :param user: The user parameter is the owner of the cart. It is used to retrieve the cart object
    associated with the user
    :return: all the products in the user's cart.
    """
    cart = Cart.objects.get(owner=user)
    return cart.products.all()


def get_vendors(cart_products, product_ids=None):
    """
    The function `get_vendors` returns a list of unique vendors from a user's cart, based on the product
    IDs provided.

    :param cart_products: The `cart_products` parameter is a list of objects representing the products
    in the user's cart. Each object has a `product` attribute which contains information about the
    product, including the `owner` attribute which represents the vendor of the product
    :param product_ids: The `product_ids` parameter is a list of specific product IDs. If this parameter
    is provided, the function will only consider cart products with matching product IDs when
    determining the vendors. If `product_ids` is not provided, the function will consider all cart
    products
    :return: a list of vendors.
    """
    # append all vendor exist in user's cart
    vendors = []
    if product_ids:
        [vendors.append(cart_product.product.owner)
         for cart_product in cart_products if cart_product.product.owner not in vendors and cart_product.product.id in product_ids]
    else:
        [vendors.append(cart_product.product.owner)
            for cart_product in cart_products if cart_product.product.owner not in vendors]
    return vendors


def get_products_by_vendor(vendors, cart_products):
    """
    The function `get_products_by_vendor` groups cart products by vendor.

    :param vendors: A list of vendor objects. Each vendor object has an 'id' attribute
    :param cart_products: The `cart_products` parameter is a list of products in the user's shopping
    cart. Each product in the list has an attribute `product.owner` which represents the vendor who owns
    the product
    :return: a dictionary where the keys are the IDs of the vendors and the values are dictionaries
    containing the vendor object and a list of cart products associated with that vendor.
    """
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
    return products_by_vendor


def calc_total_price(cart_products):
    """
    The function calculates the total price of products in a shopping cart.

    :param cart_products: The `cart_products` parameter is a list of objects representing products in a
    shopping cart. Each object in the list has two attributes: `product` and `quantity`. The `product`
    attribute represents the product being purchased and has a `price` attribute, which represents the
    price of the product
    :return: the total price of all the products in the cart.
    """
    total_price = 0
    for cart_product in cart_products:
        total_price = total_price + \
            (cart_product.product.price * cart_product.quantity)
    return total_price


@csrf_exempt
def checkout(request):
    """
    The `checkout` function handles the checkout process for a user, based on the mode specified in the
    request.

    :param request: The `request` parameter is an object that represents the HTTP request made by the
    client. It contains information such as the request method (e.g., GET, POST), the request data
    (e.g., form data, query parameters), and the user making the request
    :return: an HttpResponse object.
    """
    if request.method != "POST":
        return HttpResponse('Invalid request')
    try:
        mode = request.POST['mode']
    except:
        return HttpResponse('Invalid request')
    if mode == 'all':
        cart_products = get_cart_products(request.user)
        vendors = get_vendors(cart_products)
        products_by_vendor = get_products_by_vendor(vendors, cart_products)
        total_price = calc_total_price(cart_products)
    elif mode == 'selected':
        try:
            product_ids = [
                int(product_id) for product_id in request.POST["product_ids"].split(",") if product_id != ""]
        except:
            return HttpResponse("Invalid request")
        cart_products = get_cart_products(request.user)
        vendors = get_vendors(cart_products, product_ids)
        products_by_vendor = get_products_by_vendor(vendors, cart_products)
        total_price = calc_total_price(cart_products)
    elif mode == 'buy_now':
        product = Product.objects.get(id=request.POST["product_id"])
        quantity = int(request.POST["quantity"])
        products_by_vendor = {
            product.owner.id: {
                'vendor': product.owner,
                'cart_products': [
                    {
                        'product': product,
                        'quantity': quantity
                    }],
            }
        }
        total_price = product.price * quantity
    else:
        return HttpResponse('Invalid request')

    template = loader.get_template("order/checkout.html")
    context = {
        "username": request.user.username,
        "cart_quantity": request.user.cart_quantity,
        "type": request.user.account_type,
        "products_by_vendor": products_by_vendor,
        "total_price": round(total_price, 2)
    }
    return HttpResponse(template.render(context, request))


def place_order(request):
    if request.method != "POST":
        return HttpResponse('Invalid request')
    try:
        mode = request.POST['mode']
    except:
        return HttpResponse('Invalid request')
    if mode == 'all':
        cart_products = get_cart_products(request.user)
        vendors = get_vendors(cart_products)
        products_by_vendor = get_products_by_vendor(vendors, cart_products)
        total_price = calc_total_price(cart_products)
    elif mode == 'selected':
        try:
            product_ids = [
                int(product_id) for product_id in request.POST["product_ids"].split(",") if product_id != ""]
        except:
            return HttpResponse("Invalid request")
        cart_products = get_cart_products(request.user)
        vendors = get_vendors(cart_products, product_ids)
        products_by_vendor = get_products_by_vendor(vendors, cart_products)
        total_price = calc_total_price(cart_products)
    elif mode == 'buy_now':
        product = Product.objects.get(id=request.POST["product_id"])
        quantity = int(request.POST["quantity"])
        products_by_vendor = {
            product.owner.id: {
                'vendor': product.owner,
                'cart_products': [
                    {
                        'product': product,
                        'quantity': quantity
                    }],
            }
        }
        total_price = product.price * quantity
    else:
        return HttpResponse('Invalid request')

    return redirect('/order/')


def view_order(request, order_id):
    template = loader.get_template("order/order.html")
    context = {
        "username": request.user.username,
        "cart_quantity": request.user.cart_quantity,
        "type": request.user.account_type
    }
    return HttpResponse(template.render(context, request))


def view_orders(request):
    template = loader.get_template("order/orders.html")
    context = {
        "username": request.user.username,
        "cart_quantity": request.user.cart_quantity,
        "type": request.user.account_type
    }
    return HttpResponse(template.render(context, request))
