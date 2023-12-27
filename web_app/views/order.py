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
    context = {
        "username": request.user.username,
        "cart_quantity": request.user.cart_quantity,
        "type": request.user.account_type,
        "mode": mode
    }

    if mode == 'all':
        cart_products = get_cart_products(request.user)
        vendors = get_vendors(cart_products)
        products_by_vendor = get_products_by_vendor(vendors, cart_products)
        total_price = calc_total_price(cart_products)
    elif mode == 'selected':
        context["product_ids"] = request.POST["product_ids"]
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
    if request.user == "guest":
        return redirect("/signin")

    if request.method == "POST":
        mode = request.POST['mode']
        context = parse_checkout_context(request, mode)
        request.session['context'] = context
    elif request.method == "GET":
        context = request.session.get('context')
        if context['from_add'] == True:
            mode = context['mode']
        del request.session['context']
    else:
        return HttpResponse('Invalid request')

    template = loader.get_template("order/checkout.html")
    return HttpResponse(template.render(context, request))


def place_order(request):
    if request.method != "POST":
        return HttpResponse('Invalid request')
    elif request.user == "guest":
        return redirect("/signin")

    try:
        mode = request.POST['mode']
    except:
        return HttpResponse('Invalid request')

    address = Address.objects.get(id=request.POST["address_id"])
    card = Card.objects.get(id=request.POST["card_id"])

    if mode == 'all':
        checkout_products = get_cart_products(request.user)
        total_price = calc_total_price(checkout_products)

        order = Order(owner=request.user, products=checkout_products, address=address,
                      card=card, total_price=total_price, status="A")

        # clear all products from user cart
        # cart = Cart.objects.get(owner=request.user)
        # cart.products.clear()
    elif mode == 'selected':
        try:
            product_ids = [
                int(product_id) for product_id in request.POST["product_ids"].split(",") if product_id != ""]
        except:
            return HttpResponse("Invalid request")

        cart_products = get_cart_products(request.user)
        total_price = calc_total_price(cart_products)

        order = Order(owner=request.user, address=address,
                      card=card, total_price=total_price, status="A")

        cart = Cart.objects.get(owner=request.user)
        for cart_product in cart_products:
            if cart_product.id in product_ids:
                order.products.create(
                    product=cart_product.product, quantity=cart_product.quantity)
                cart.products.remove(cart_product)

    elif mode == 'buy_now':
        product = Product.objects.get(id=request.POST["product_id"])
        quantity = int(request.POST["quantity"])
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
