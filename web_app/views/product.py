from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.db.models import Max
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage

from web_app.models import Product, User

from thefuzz import process

from os import getcwd, listdir, remove
from shutil import rmtree

fs = FileSystemStorage()


def fuzzy_search(search_query, products_input):
    product_names = products_input.values_list('name', flat=True)

    # query search with fuzzy matching
    best_matches = process.extractBests(
        search_query, product_names, score_cutoff=70, limit=60)
    best_match_names = [match[0] for match in best_matches]

    # add items that contain the search query as a substring
    for product_name in product_names:
        if search_query.lower() in product_name.lower():
            best_match_names.append(product_name)

    best_match_names = list(set(best_match_names))  # remove duplicates

    if best_match_names == []:
        products = None
        max_price = 0
    else:
        products = products_input.filter(name__in=best_match_names)
        max_price = products.aggregate(Max('price'))['price__max']

    return products, max_price


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

    if request.GET.get('search') and request.GET.get('filter'):
        # If the filter is 'price'
        if request.GET.get('filter') == 'price':
            context['active_filter'] = 'price'
            products = products_list
            context['max_filter'] = int(request.GET.get('max'))
            context['min_filter'] = int(request.GET.get('min'))
        # If the filter is other (category)
        else:
            products = products_list.filter(category=request.GET.get('filter'))
            context['active_filter'] = request.GET.get('filter')

        search_query = request.GET.get('search')
        products, max_price = fuzzy_search(search_query, products)

    # If there is a search query in the request
    elif request.GET.get('search'):
        context['active_filter'] = 'search'
        search_query = request.GET.get('search')
        products, max_price = fuzzy_search(search_query, products_list)

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

    template = loader.get_template("product/listing.html")
    return HttpResponse(template.render(context, request))


def listing_vendor(request, vendor):
    """
    The function "listing_vendor" retrieves a list of products owned by a specific vendor and renders
    them in a template.

    :param request: The request object contains information about the current HTTP request, such as the
    method (GET, POST, etc.) and user information
    :param vendor: The "vendor" parameter is the username of the vendor whose products we want to list
    :return: an HttpResponse object.
    """
    if request.method != "GET":
        return HttpResponse('Invalid request')

    context = {
        "username": request.user.username,
        "cart_quantity": request.user.cart_quantity,
        "type": request.user.account_type
    }

    try:
        vendor = User.objects.get(username=vendor)
    except:
        return HttpResponse('Not found')
    products = Product.objects.filter(owner=vendor)
    context['products'] = products

    template = loader.get_template("product/vendor-listing.html")
    return HttpResponse(template.render(context, request))


def view_product(request, product_id):
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

    try:
        product = Product.objects.get(id=product_id)
    except:
        return HttpResponse('Invalid product id')

    context["product_id"] = product.id
    context["category"] = product.category
    context["name"] = product.name
    context["price"] = product.price
    context["description"] = product.description
    context["images"] = product.images
    context["vendor_name"] = product.owner.name
    context["vendor_username"] = product.owner.username
    context["vendor_avatar"] = product.owner.avatar

    related_products = []
    products = Product.objects.filter(
        category=product.category).order_by('?')
    for p in products:
        if p.id != product.id:
            related_products.append(p)
    context['related_products'] = related_products[:8]

    if product.owner == request.user:
        template = loader.get_template("product/vendor-product.html")
    else:
        template = loader.get_template("product/product.html")
    return HttpResponse(template.render(context, request))


@csrf_exempt
def add_product(request):
    """
    The `add_product` function handles the logic for adding a new product to the system, including
    validating the user's account type, retrieving categories for the product, and saving the product
    details and images.

    :param request: The `request` parameter is an object that represents the HTTP request made by the
    user. It contains information about the request, such as the user making the request, the method
    used (GET or POST), and any data sent with the request
    :return: an HttpResponse object or redirects to another page.
    """
    if request.user.account_type != "V":
        return HttpResponse('You are not a vendor')

    context = {
        "username": request.user.username,
        "cart_quantity": request.user.cart_quantity,
        "type": request.user.account_type
    }

    # If the request method is GET, retrieve categories and render the add product page
    if request.method == "GET":
        categories = Product.objects.values_list(
            'category', flat=True).distinct()
        context['categories'] = categories
        template = loader.get_template("product/add-product.html")
        return HttpResponse(template.render(context, request))

    # If the request method is POST, retrieve product details and images and save them to the database
    elif request.method == "POST":
        name = request.POST["pd-name"]
        price = float(request.POST["pd-price"])
        category = request.POST["pd-category"]
        if category == 'other':
            category = request.POST["pd-new-category"]
        description = request.POST["pd-description"]

        product = Product.objects.create(
            name=name, price=price, category=category, description=description, owner=request.user)

        images = []
        for i in range(int(request.POST["img-range"])):
            upload_img = request.FILES["preview-img-"+str(i)]
            fs.save(getcwd() + '/web_app/static/images/products/' +
                    str(product.id) + '/' + upload_img.name, upload_img)
            images.append(str(product.id) + '/' + upload_img.name)
        product.images = images
        product.save()

        return redirect('/product/'+str(product.id))
    else:
        return HttpResponse('Invalid request')


@csrf_exempt
def update_product(request, product_id):
    if request.user.account_type != "V":
        return HttpResponse('You are not a vendor')

    context = {
        "username": request.user.username,
        "cart_quantity": request.user.cart_quantity,
        "type": request.user.account_type
    }

    try:
        product = Product.objects.get(id=product_id)
    except:
        return HttpResponse('Invalid product id')

    # If the request method is GET, retrieve categories and render the update product page
    if request.method == "GET":
        context['id'] = product.id
        context['name'] = product.name
        context['price'] = product.price
        context['pd_category'] = product.category
        context['description'] = product.description
        categories = Product.objects.values_list(
            'category', flat=True).distinct()
        context['categories'] = categories
        img_range_images = zip(range(len(product.images)), product.images)
        context['img_range_images'] = img_range_images
        context['img_range'] = len(product.images)

        template = loader.get_template("product/update-product.html")
        return HttpResponse(template.render(context, request))

    # If the request method is POST, retrieve product details and images and save them to the database
    elif request.method == "POST":
        name = request.POST["pd-name"]
        price = float(request.POST["pd-price"])
        category = request.POST["pd-category"]
        if category == 'other':
            category = request.POST["pd-new-category"]
        description = request.POST["pd-description"]

        images = []
        for i in range(int(request.POST["img-range"])):
            try:
                upload_img = request.FILES["preview-img-"+str(i)]
                fs.save(getcwd() + '/web_app/static/images/products/' +
                        str(product.id) + '/' + upload_img.name, upload_img)
                images.append(str(product.id) + '/' + upload_img.name)
            except:
                images.append(request.POST["preview-img-"+str(i)])

        if images == []:
            rmtree(getcwd() + '/web_app/static/images/products/' + str(product.id))
        else:
            for image in listdir(getcwd() + '/web_app/static/images/products/' + str(product.id)):
                if str(product.id) + '/' + image not in images:
                    remove(getcwd() + '/web_app/static/images/products/' +
                           str(product.id) + '/' + image)

        product.name = name
        product.price = price
        product.category = category
        product.description = description
        product.images = images
        product.save()

        return redirect('/product/'+str(product.id))
    else:
        return HttpResponse('Invalid request')


@csrf_exempt
def delete_product(request, product_id):
    """
    This function deletes a product if the request is a POST request and the user is a vendor.

    :param request: The `request` parameter is an object that represents the HTTP request made by the
    client. It contains information such as the request method (e.g., GET, POST), user session, user
    agent, and more
    :param product_id: The product_id parameter is the unique identifier of the product that needs to be
    deleted
    :return: an HttpResponse object or redirecting to a specific URL.
    """
    if request.method != "POST":
        return HttpResponse('Invalid request')
    elif request.user.account_type != "V":
        return HttpResponse('You are not a vendor')

    product = Product.objects.get(id=product_id)
    if product.owner == request.user:
        rmtree(getcwd() + '/web_app/static/images/products/' + str(product.id))
        product.delete()
    else:
        return HttpResponse('You are not the owner of this product')
    return redirect('/products/vendor/' + request.user.username)
