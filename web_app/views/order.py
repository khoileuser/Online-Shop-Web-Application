from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from web_app.models import Cart, User, Product
from django.views.decorators.csrf import csrf_exempt


def get_cart_products(user):
    cart = Cart.objects.get(owner=user)
    return cart.products.all()


def get_vendors(cart_products, product_ids=None):
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
        _cart_products = [
            cart_product for cart_product in cart_products if cart_product.product.owner == vendor]
        products_by_vendor[vendor.id] = {
            'vendor': vendor,
            'cart_products': _cart_products,
        }
    return products_by_vendor


def calc_total_price(cart_products):
    total_price = 0
    for cart_product in cart_products:
        total_price = total_price + \
            (cart_product.product.price * cart_product.quantity)
    return total_price


@csrf_exempt
def checkout(request):
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
