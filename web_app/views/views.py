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
    from web_app.models import User
    print(User.objects.all().values())
    # User.objects.get(id=2).delete()
    return HttpResponse('ok')


def seeding():
    shop_owners = ['EleForge', 'Metal Plate', 'Urban Thread', 'Horizon Haven', 'Feathers & Whispers', 'Wonder Writebooks', 'The Traveller',
                   'Elixie Buff', 'Shoes Empire', 'Game On!', 'D&C', 'Leaking Time', 'BoostLife', 'Motor Glory', 'Canvas Attack']

    import os
    import json
    from web_app.models import Product, User

    with open('web_app/products.json', 'r', encoding="utf-8") as f:
        categories = json.load(f)

    i = 0
    for category in categories:
        for product in categories[category]:
            owner = User.objects.get(name=shop_owners[i])
            name = categories[category][product]['name']
            price = categories[category][product]['price']
            description = categories[category][product]['description']
            images = categories[category][product]['images']

            print(owner)
            print(name)
            print(str(float(price)))
            print(description)
            print(images)
            print('---------------------')

            product = Product(owner=owner, name=name, price=float(price),
                              description=description, images=images, category=category)
            product.save()
        i += 1

    return HttpResponse('ok')
