from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from web_app.models import Product

import random


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
    products = Product.objects.all().order_by('?')[:18]
    context['trending1'] = list(products.values())[:3]
    context['trending2'] = list(products.values())[3:7]
    context['trending3'] = list(products.values())[7:10]
    context['new_arrival1'] = list(products.values())[10:14]
    context['new_arrival2'] = list(products.values())[14:18]
    context['new_arrival3'] = list(products.values())[18:22]
    return HttpResponse(template.render(context, request))


def execute_(request):
    from web_app.models import Product, User
    # print(Product.objects.all().values())
    print(User.objects.all().values())
    # User.objects.get(id=1).delete()
    return HttpResponse('ok')


def execute(request):
    import os
    import json
    from web_app.models import Product, User

    # for product in os.listdir('./web_app/static/images/products'):
    #     print(product)
    #     images = []
    #     for image in os.listdir('./web_app/static/images/products/' + product):
    #         images.append(product + '/' + image)
    #     print(images)
    #     pd = Product.objects.get(id=int(product))
    #     pd.images = images
    #     pd.save()

    products = Product.objects.all()
    for product in products:
        for image in product.images:
            if os.path.exists(f'./web_app/static/images/products/{image}') == False:
                print(product)
                print(image)

    return HttpResponse('ok')
