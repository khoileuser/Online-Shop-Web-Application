from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


def index(request):
    template = loader.get_template("index.html")
    if request.user != "guest":
        context = {
            "username": request.user.username,
            "cart_quantity": request.user.cart_quantity
        }
    else:
        context = {
            "username": None,
            "cart_quantity": None
        }
    return HttpResponse(template.render(context, request))


def execute(request):
    # from web_app.models import User
    # print(User.objects.all().values())
    # User.objects.get(id=2).delete()
    # return HttpResponse('ok')

    from web_app.models import Cart

    products = Cart.objects().get(owner=request.user).products
    print(products)

    return

    categories = ['Electronic accessory', 'Kitchen', 'Fashion', 'House', 'Baby', 'Books', 'Luggage',
                  'Beauty', 'Shoes', 'Pet supplies', 'Sport']

    not_done = ['Healthcare', 'Watches', 'Automotive', 'Arts & Crafts']

    import xlwings as xw
    import os
    from fuzzywuzzy import process
    from web_app.models import Product

    for category in categories:
        ws = xw.Book(
            "products.xlsx").sheets[category]

        names = ws.range("A2:A31").value
        prices = ws.range("B2:B31").value
        description = ws.range("C2:C31").value

        for i in range(0, 29):
            print("Name:", names[i])
            print("Price:", prices[i])
            print("Description:", description[i])

            products = []
            for product in os.listdir('web_app/static/images/products/' + category):
                products.append(product)
            matched_product = process.extractOne(
                names[i], products)

            images = []
            for image in os.listdir('web_app/static/images/products/' + category + '/' + matched_product[0]):
                images.append('web_app/static/images/products/' +
                              category + '/' + matched_product[0] + '/' + image)
            break

        # product = Product(
        #     owner=None, name=names[i], price=prices[i], description=description[i], images=images, category=category)
        # product.save()

    return HttpResponse('ok')
