from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.db.models import Max
from web_app.models import Product, User


def listing(request):
    if request.method != "GET":
        return HttpResponse('Invalid request')
    elif request.user != "guest":
        context = {
            "username": request.user.username,
            "cart_quantity": request.user.cart_quantity,
            "type": request.user.account_type
        }
    else:
        context = {
            "username": None,
            "cart_quantity": None,
            "type": None
        }

    _products = Product.objects
    categories = _products.values_list('category', flat=True).distinct()
    context['categories'] = categories
    products_list = _products.all().order_by('?')

    if request.GET.get('search'):
        context['active_filter'] = 'search'
    elif request.GET.get('filter'):
        if request.GET.get('filter') == 'price':
            context['active_filter'] = 'price'
            products = products_list
            context['max_filter'] = int(request.GET.get('max'))
            context['min_filter'] = int(request.GET.get('min'))
            max_price = products_list.aggregate(Max('price'))['price__max']
            context['max_price'] = max_price
            context['min_price'] = max_price-1
        else:
            products = products_list.filter(category=request.GET.get('filter'))
            context['active_filter'] = request.GET.get('filter')
            max_price = products.aggregate(Max('price'))['price__max']
            context['max_price'] = max_price
            context['min_price'] = max_price-1
    else:
        paginator = Paginator(products_list, 30)
        context['page_range'] = paginator.page_range
        page_number = request.GET.get('page')
        context['active_page'] = page_number
        products = paginator.get_page(page_number)
        max_price = products_list.aggregate(Max('price'))['price__max']
        context['max_price'] = max_price
        context['min_price'] = max_price-1

    context['products'] = products

    template = loader.get_template("products/listing.html")
    return HttpResponse(template.render(context, request))


def listing_vendor(request, vendor):
    if request.method != "GET":
        return HttpResponse('Invalid request')
    elif request.user != "guest":
        context = {
            "username": request.user.username,
            "cart_quantity": request.user.cart_quantity,
            "type": request.user.account_type
        }
    else:
        context = {
            "username": None,
            "cart_quantity": None,
            "type": None
        }

    vendor = User.objects.get(username=vendor)
    products = Product.objects.filter(vendor=vendor)
    context['products'] = products

    template = loader.get_template("products/listing.html")
    return HttpResponse(template.render(context, request))


def product(request, product_id):
    """
    The function "product" retrieves information about a specific product and renders it in a template,
    along with additional context data such as the user's username, cart quantity, and account type.

    :param request: The request parameter is an object that represents the HTTP request made by the
    user. It contains information such as the user's session, cookies, headers, and other data related
    to the request
    :param product_id: The product_id parameter is the unique identifier of the product that is being
    requested. It is used to retrieve the specific product from the database
    :return: an HttpResponse object.
    """
    if request.method != "GET":
        return HttpResponse('Invalid request')
    elif request.user != "guest":
        context = {
            "username": request.user.username,
            "cart_quantity": request.user.cart_quantity,
            "type": request.user.account_type
        }
    else:
        context = {
            "username": None,
            "cart_quantity": None,
            "type": None
        }
    product = Product.objects.get(id=product_id)
    context["product_id"] = product.id
    context["category"] = product.category
    context["name"] = product.name
    context["price"] = product.price
    context["description"] = product.description
    context["images"] = product.images

    template = loader.get_template("products/product.html")
    return HttpResponse(template.render(context, request))


def add_product(request):
    template = loader.get_template("product-management/addproduct.html")
    return HttpResponse(template.render())


def update_product(request):
    template = loader.get_template("product-management/updateproduct.html")
    return HttpResponse(template.render())
