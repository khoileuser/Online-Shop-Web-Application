from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from web_app.models import Cart, Product, Order, Address, Card
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict

from web_app.data import *


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
    The function `get_products_by_vendor` groups cart products by vendor and returns a dictionary with
    vendor information and their respective cart products.

    :param vendors: A list of vendor objects. Each vendor object has attributes like id, name, and
    username
    :param cart_products: The `cart_products` parameter is a list of products in the user's shopping
    cart. Each product in the list is an object that has a `product` attribute, which represents the
    actual product being sold, and an `owner` attribute, which represents the vendor who owns the
    product
    :return: a dictionary where the keys are the IDs of the vendors and the values are dictionaries
    containing information about the vendor and their associated products in the cart.
    """
    # group vendor
    products_by_vendor = {}
    for vendor in vendors:
        # group products by vendor
        _cart_products = []
        for cart_product in cart_products:
            if cart_product.product.owner == vendor:
                product_dict = model_to_dict(cart_product)
                product_dict['product'] = model_to_dict(cart_product.product)
                _cart_products.append(product_dict)
        products_by_vendor[vendor.id] = {
            'vendor': {
                "name": vendor.name,
                "username": vendor.username
            },
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


def parse_checkout_context(request, mode):
    """
    The function `parse_checkout_context` takes in a request and a mode, and returns a context
    dictionary containing user details, mode, total price, products by vendor, and default address and
    card information.

    :param request: The `request` parameter is an object that represents the HTTP request made by the
    user. It contains information such as the user making the request, the POST data sent with the
    request, and other metadata
    :param mode: The "mode" parameter is a string that determines the calculation mode for the checkout
    context. It can have one of the following values:
    :return: a context dictionary containing various information related to the checkout process, such
    as user details, mode, total price, products by vendor, default address, and default card.
    """
    # Initialize the context with user details and mode
    context = {
        "username": request.user.username,
        "cart_quantity": request.user.cart_quantity,
        "type": request.user.account_type,
        "mode": mode
    }

    # If mode is 'all', calculate total price for all products in the cart
    if mode == 'all':
        cart_products = get_cart_products(request.user)
        vendors = get_vendors(cart_products)
        products_by_vendor = get_products_by_vendor(vendors, cart_products)
        total_price = calc_total_price(cart_products)

    # If mode is 'selected', calculate total price for selected products in the cart
    elif mode == 'selected':
        context["product_ids"] = request.POST["product_ids"]
        product_ids = [int(product_id) for product_id in request.POST["product_ids"].split(
            ",") if product_id != ""]
        cart_products = get_cart_products(request.user)
        vendors = get_vendors(cart_products, product_ids)
        products_by_vendor = get_products_by_vendor(vendors, cart_products)
        total_price = calc_total_price(cart_products)

    # If mode is 'buy_now', calculate total price for the single product being bought now
    elif mode == 'buy_now':
        context["product_id"] = request.POST["product_id"]
        context["quantity"] = request.POST["quantity"]
        product = Product.objects.get(id=request.POST["product_id"])
        quantity = int(request.POST["quantity"])
        products_by_vendor = {
            product.owner.id: {
                'vendor': {
                    "name": product.owner.name,
                    "username": product.owner.username
                },
                'cart_products': [
                    {
                        'product': model_to_dict(product),
                        'quantity': quantity
                    }],
            }
        }
        total_price = product.price * quantity

    context["products_by_vendor"] = products_by_vendor
    context["total_price"] = round(total_price, 2)

    _address = None
    _card = None

    for address in request.user.addresses.all():
        if address.is_default:
            _address = address
            break

    for card in request.user.cards.all():
        if card.is_default:
            expiration_date = month_map[card.expiration_date[:2]
                                        ] + ' 20' + card.expiration_date[-2:]
            _card = {
                'id': card.id,
                'card_type': card.card_type,
                'card_number': card.card_number[-4:],
                'expiration_date': expiration_date,
                'is_default': card.is_default
            }
            break

    context['address'] = model_to_dict(_address) if _address else None
    context['card'] = _card

    if not _address:
        context['names'] = names_data
        context['phones'] = phones_data

    return context


@csrf_exempt
def checkout(request):
    """
    The `checkout` function handles the checkout process for a user, redirecting them to sign in if they
    are a guest, parsing the checkout context from the request, and rendering the checkout template with
    the context.

    :param request: The `request` parameter is an object that represents the HTTP request made by the
    client. It contains information about the request, such as the method (GET, POST, etc.), headers,
    user information, and any data sent with the request
    :return: an HttpResponse object.
    """
    if request.user == "guest":
        return redirect("/signin")

    if request.method == "POST":
        mode = request.POST['mode']
        context = parse_checkout_context(request, mode)
        request.session['context'] = context
    elif request.method == "GET":
        context = request.session.get('context')
    else:
        return HttpResponse('Invalid request')

    template = loader.get_template("order/checkout.html")
    return HttpResponse(template.render(context, request))


def place_order(request):
    if request.method != "POST":
        return HttpResponse('Invalid request')
    elif request.user == "guest":
        return redirect("/signin")

    context = request.session.get('context')
    del request.session['context']

    address = Address.objects.get(id=context["address_id"])
    card = Card.objects.get(id=context["card_id"])

    if context["mode"] == 'all':
        checkout_products = get_cart_products(request.user)
        total_price = calc_total_price(checkout_products)

        order = Order(owner=request.user, products=checkout_products, address=address,
                      card=card, total_price=total_price, status="A")

        # clear all products from user cart
        cart = Cart.objects.get(owner=request.user)
        cart.products.clear()
    elif context["mode"] == 'selected':
        product_ids = [int(product_id) for product_id in context["product_ids"].split(
            ",") if product_id != ""]

        cart_products = get_cart_products(request.user)
        total_price = calc_total_price(cart_products)

        order = Order(owner=request.user, address=address,
                      card=card, total_price=total_price, status="A")

        # clear selected products from user cart
        cart = Cart.objects.get(owner=request.user)
        for cart_product in cart_products:
            if cart_product.id in product_ids:
                order.products.create(
                    product=cart_product.product, quantity=cart_product.quantity)
                cart.products.remove(cart_product)
    elif context["mode"] == 'buy_now':
        product = Product.objects.get(id=context["product_id"])
        quantity = int(context["quantity"])
        total_price = product.price * quantity

        order = Order(owner=request.user, address=address,
                      card=card, total_price=total_price, status="A")
        order.products.create(product=product, quantity=quantity)
    else:
        return HttpResponse('Invalid request')

    return redirect('/order/' + order.id)


def view_order(request, order_id):
    if request.method != "POST":
        return HttpResponse('Invalid request')
    elif request.user == "guest":
        return redirect("/signin")

    order = Order.objects.get(id=order_id)

    template = loader.get_template("order/order.html")
    context = {
        "username": request.user.username,
        "cart_quantity": request.user.cart_quantity,
        "type": request.user.account_type,
    }
    return HttpResponse(template.render(context, request))


def view_orders(request):
    if request.method != "POST":
        return HttpResponse('Invalid request')
    elif request.user == "guest":
        return redirect("/signin")

    template = loader.get_template("order/orders.html")
    context = {
        "username": request.user.username,
        "cart_quantity": request.user.cart_quantity,
        "type": request.user.account_type
    }
    return HttpResponse(template.render(context, request))
