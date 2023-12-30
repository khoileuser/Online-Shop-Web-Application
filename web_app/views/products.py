from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.db.models import Max
from web_app.models import Product, User

from thefuzz import process


def listing(request):
    """
    The `listing` function is a view function in Django that handles the rendering of a product listing
    page, including filtering and searching functionality.

    :param request: The `request` parameter is an object that represents the HTTP request made by the
    client. It contains information such as the request method (GET, POST, etc.), user information, and
    any data sent with the request
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

    # get all products and categories
    _products = Product.objects
    categories = _products.values_list('category', flat=True).distinct()
    context['categories'] = categories
    products_list = _products.all().order_by('?')

    # If there is a search query in the request
    if request.GET.get('search'):
        context['active_filter'] = 'search'
        search_query = request.GET.get('search')
        product_names = _products.values_list('name', flat=True)

        # query search with fuzzy matching
        best_matches = process.extractBests(
            search_query, product_names, score_cutoff=60, limit=60)
        best_match_names = [match[0] for match in best_matches]
        if best_match_names == []:
            products = None
            max_price = 0
        else:
            products = _products.filter(name__in=best_match_names)
            max_price = products.aggregate(Max('price'))['price__max']

    # If there is a filter in the request
    elif request.GET.get('filter'):
        # If the filter is 'price'
        if request.GET.get('filter') == 'price':
            context['active_filter'] = 'price'
            products = products_list
            context['max_filter'] = int(request.GET.get('max'))
            context['min_filter'] = int(request.GET.get('min'))
            max_price = products_list.aggregate(Max('price'))['price__max']
        # If the filter is other (category)
        else:
            products = products_list.filter(category=request.GET.get('filter'))
            context['active_filter'] = request.GET.get('filter')
            max_price = products.aggregate(Max('price'))['price__max']

    # If there is no search query or filter in the request, return with pagination
    else:
        paginator = Paginator(products_list, 30)
        context['page_range'] = paginator.page_range
        page_number = request.GET.get('page')
        context['active_page'] = page_number
        products = paginator.get_page(page_number)
        max_price = products_list.aggregate(Max('price'))['price__max']

    context['products'] = products
    context['max_price'] = max_price
    context['min_price'] = max_price-1

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
