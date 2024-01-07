from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict

from web_app.models import Cart, Product, Order, Address, Card
from web_app.data import *


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
    products_by_vendor = []
    for vendor in vendors:
        # group products by vendor
        _cart_products = []
        for cart_product in cart_products:
            if cart_product.product.owner == vendor:
                product_dict = model_to_dict(cart_product)
                product_dict['product'] = model_to_dict(cart_product.product)
                _cart_products.append(product_dict)
        products_by_vendor.append({
            'vendor': {
                "id": vendor.id,
                "name": vendor.name,
                "username": vendor.username
            },
            'cart_products': _cart_products,
        })
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
        cart_products = Cart.objects.get(
            owner=request.user).products.all().order_by('id')
        vendors = get_vendors(cart_products)
        products_by_vendor = get_products_by_vendor(vendors, cart_products)
        total_price = calc_total_price(cart_products)

    # If mode is 'selected', calculate total price for selected products in the cart
    elif mode == 'selected':
        context["product_ids"] = request.POST["product_ids"]
        product_ids = [int(product_id) for product_id in request.POST["product_ids"].split(
            ",") if product_id != ""]
        cart_products = Cart.objects.get(
            owner=request.user).products.all().order_by('id')
        vendors = get_vendors(cart_products, product_ids)
        products_by_vendor = get_products_by_vendor(vendors, cart_products)
        total_price = calc_total_price(cart_products)

    # If mode is 'buy_now', calculate total price for the single product being bought now
    elif mode == 'buy_now':
        context["product_id"] = request.POST["product_id"]
        context["quantity"] = request.POST["quantity"]
        product = Product.objects.get(id=request.POST["product_id"])
        quantity = int(request.POST["quantity"])
        products_by_vendor = [{
            'vendor': {
                "id": product.owner.id,
                "name": product.owner.name,
                "username": product.owner.username
            },
            'cart_products': [
                {
                    'product': model_to_dict(product),
                    'quantity': quantity
                }],
        }]
        total_price = product.price * quantity

    context["products_by_vendor"] = products_by_vendor
    context["total_price"] = round(total_price, 2)

    _address = None
    _card = None
    addresses = []
    cards = []

    # get default address
    for address in request.user.addresses.all():
        if address.is_default:
            _address = address
        addresses.append(model_to_dict(address))

    # get default card
    for card in request.user.cards.all():
        # reparse card info to prevent security issues
        expiration_date = month_map[card.expiration_date[:2]
                                    ] + ' 20' + card.expiration_date[-2:]
        _card_ = {
            'id': card.id,
            'card_type': card.card_type,
            'card_number': card.card_number[-4:],
            'expiration_date': expiration_date,
            'is_default': card.is_default
        }
        if card.is_default:
            _card = _card_
        cards.append(_card_)

    context['address'] = model_to_dict(_address) if _address else None
    context['card'] = _card
    context['addresses'] = addresses
    context['cards'] = cards

    # get names and phones for adding new address
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
    elif request.user.account_type != "C":
        return HttpResponse('You are not a customer')

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


@csrf_exempt
def checkout_change(request, field):
    """
    The function `checkout_change` handles the checkout process by updating the address or card
    information based on the user's request.

    :param request: The `request` parameter is an object that represents the HTTP request made by the
    client. It contains information such as the request method (e.g., GET, POST), user information,
    session data, and other request-specific details
    :param field: The "field" parameter is a string that specifies which field is being updated in the
    checkout process. It can have two possible values: "address" or "card"
    :return: a redirect response to the previous page.
    """
    if request.method != "POST":
        return HttpResponse('Invalid request')
    elif request.user == "guest":
        return redirect("/signin")
    elif request.user.account_type != "C":
        return HttpResponse('You are not a customer')

    context = request.session.get('context')
    if field == 'address':
        address = Address.objects.get(id=request.POST['address_id'])
        context['address'] = model_to_dict(address)
    elif field == 'card':
        card = Card.objects.get(id=request.POST['card_id'])
        expiration_date = month_map[card.expiration_date[:2]
                                    ] + ' 20' + card.expiration_date[-2:]
        context['card'] = {
            'id': card.id,
            'card_type': card.card_type,
            'card_number': card.card_number[-4:],
            'expiration_date': expiration_date,
            'is_default': card.is_default
        }

    request.session['context'] = context

    return redirect(request.META['HTTP_REFERER'])


@csrf_exempt
def place_order(request):
    """
    The `place_order` function processes a user's order by retrieving the necessary information from the
    request and session, creating a new order with the selected products, updating the user's cart, and
    redirecting to the order details page.

    :param request: The `request` parameter is an object that represents the HTTP request made by the
    client. It contains information such as the request method (e.g., GET, POST), user information,
    session data, and other request-specific details
    :return: a redirect response to the URL '/order/' followed by the ID of the created order.
    """
    if request.method != "POST":
        return HttpResponse('Invalid request')
    elif request.user == "guest":
        return redirect("/signin")
    elif request.user.account_type != "C":
        return HttpResponse('You are not a customer')

    # retrieve the context from the session and delete it from the session
    context = request.session.get('context')
    del request.session['context']

    # retrieve the address and card from the database using the ids stored in the context
    address = Address.objects.get(id=context["address"]["id"])
    card = Card.objects.get(id=context["card"]["id"])

    # If the mode is 'all', process all products in the cart
    if context["mode"] == "all":
        # retrieve the user's cart and all products in it
        cart = Cart.objects.get(owner=request.user)
        checkout_products = cart.products.all().order_by('id')

        # calc total price of all products in the cart
        total_price = calc_total_price(checkout_products)

        # create a new order with all products in the cart
        order = Order(owner=request.user, address=address,
                      card=card, total_price=total_price, status="A")
        order.save()
        order.products.set(checkout_products)

        # update product stock
        for cart_product in checkout_products:
            cart_product.product.stock -= cart_product.quantity
            if cart_product.product.stock < 0:
                cart_product.product.stock = 0
            cart_product.product.save()

        # clear all products from the user's cart
        cart.products.clear()

        # reset the user's cart quantity to 0
        user = request.user
        user.cart_quantity = 0
        user.save()

    # If the mode is 'selected', process only the selected products
    elif context["mode"] == "selected":
        cart = Cart.objects.get(owner=request.user)

        # filter selected cart products
        product_ids = [int(product_id) for product_id in context["product_ids"].split(
            ",") if product_id != ""]
        checkout_products = []
        cart_products = cart.products.all().order_by('id')
        for cart_product in cart_products:
            if cart_product.product.id in product_ids:
                checkout_products.append(cart_product)

        # calc total price of selected products
        total_price = calc_total_price(checkout_products)

        # create a new order
        order = Order(owner=request.user, address=address,
                      card=card, total_price=total_price, status="A")
        order.save()

        # add and remove selected products to order and from user cart
        cart = Cart.objects.get(owner=request.user)
        for checkout_product in checkout_products:
            order.products.create(
                product=checkout_product.product, quantity=checkout_product.quantity)
            cart.products.remove(checkout_product)

            # update product stock
            checkout_product.product.stock -= checkout_product.quantity
            if checkout_product.product.stock < 0:
                checkout_product.product.stock = 0
            checkout_product.product.save()

        # update user cart quantity
        user = request.user
        user.cart_quantity = cart.products.count()
        user.save()

    # If the mode is 'buy_now', process the single product being bought now
    elif context["mode"] == "buy_now":
        # get product and quantity from context and calc total price
        product = Product.objects.get(id=context["product_id"])
        quantity = int(context["quantity"])
        total_price = product.price * quantity

        # create a new order with the single product
        order = Order(owner=request.user, address=address,
                      card=card, total_price=total_price, status="A")
        order.save()
        order.products.create(product=product, quantity=quantity)

        # update product stock
        product.stock -= quantity
        if product.stock < 0:
            product.stock = 0
        product.save()
    else:
        return HttpResponse('Invalid request')

    return JsonResponse({'redirectUrl': '/order/' + str(order.id)})


def view_order(request, order_id):
    """
    The `view_order` function retrieves and displays order details for a specific order ID, including
    the products, vendors, total price, address, and card information.

    :param request: The `request` parameter is an object that represents the HTTP request made by the
    user. It contains information such as the request method (GET, POST, etc.), user authentication
    details, and any data sent with the request
    :param order_id: The order_id parameter is the unique identifier of the order that the user wants to
    view
    :return: an HttpResponse object.
    """
    if request.method != "GET":
        return HttpResponse('Invalid request')
    elif request.user == "guest":
        return redirect("/signin")
    elif request.user.account_type != "C":
        return HttpResponse('You are not a customer')

    order = Order.objects.get(id=order_id)
    if order.owner != request.user:
        return HttpResponse('You are not the owner of this order')

    vendors = get_vendors(order.products.all().order_by('id'))
    products_by_vendor = get_products_by_vendor(
        vendors, order.products.all().order_by('id'))
    expiration_date = month_map[order.card.expiration_date[:2]
                                ] + ' 20' + order.card.expiration_date[-2:]

    context = {
        "username": request.user.username,
        "cart_quantity": request.user.cart_quantity,
        "type": request.user.account_type,
        "products_by_vendor": products_by_vendor,
        "total_price": order.total_price,
        "status": order.status,
        "address": order.address,
        "card": {
            'id': order.card.id,
            'card_type': order.card.card_type,
            'card_number': order.card.card_number[-4:],
            'expiration_date': expiration_date,
            'is_default': order.card.is_default
        },
    }

    template = loader.get_template("order/order.html")
    return HttpResponse(template.render(context, request))


def view_orders(request):
    """
    The `view_orders` function retrieves and organizes order information for a user, including the total
    price and products grouped by vendor, and renders it in an HTML template.

    :param request: The `request` parameter is an object that represents the HTTP request made by the
    client. It contains information such as the request method (GET, POST, etc.), user information, and
    any data sent with the request. In this code snippet, the `request` object is used to check the
    request
    :return: an HttpResponse object.
    """
    if request.method != "GET":
        return HttpResponse('Invalid request')
    elif request.user == "guest":
        return redirect("/signin")
    elif request.user.account_type not in ["C", "S"]:
        return HttpResponse('You are not a customer or a shipper')

    if request.user.account_type == "C":
        _orders = Order.objects.filter(owner=request.user).order_by('id')
    elif request.user.account_type == "S":
        _orders = Order.objects.all().order_by('id')

    orders = []
    for order in _orders:
        vendors = get_vendors(order.products.all().order_by('id'))
        products_by_vendor = get_products_by_vendor(
            vendors, order.products.all().order_by('id'))

        orders.append({
            "id": order.id,
            "total_price": order.total_price,
            "status": order.status,
            "products_by_vendor": products_by_vendor,
        })

    context = {
        "username": request.user.username,
        "cart_quantity": request.user.cart_quantity,
        "type": request.user.account_type,
        "orders": orders,
    }

    template = loader.get_template("order/orders.html")
    return HttpResponse(template.render(context, request))


@csrf_exempt
def set_order_status(request, order_id, status):
    """
    The `set_order_status` function retrieves an order from the database and updates its status.

    :param request: The `request` parameter is an object that represents the HTTP request made by the
    user. It contains information such as the request method (GET, POST, etc.), user authentication
    details, and any data sent with the request
    :param order_id: The order_id parameter is the unique identifier of the order that the user wants to
    view
    :return: an HttpResponse object.
    """
    if request.method != "POST":
        return HttpResponse('Invalid request')
    elif request.user == "guest":
        return redirect("/signin")
    elif request.user.account_type != "S":
        return HttpResponse('You are not a shipper')

    order = Order.objects.get(id=order_id)
    if status not in ["G", "D", "C"]:
        return HttpResponse('Invalid status')
    order.status = status
    order.save()

    return redirect(request.META['HTTP_REFERER'])
