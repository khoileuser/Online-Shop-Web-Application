from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from web_app.models import User
from django.contrib.auth.hashers import make_password, check_password

import json
import os

with open(os.getcwd() + "/data/names.json", "r", encoding="utf-8") as f:
    names_data = json.load(f)

with open(os.getcwd() + "/data/phones.json", "r", encoding="utf-8") as f:
    phones_data = json.load(f)

with open(os.getcwd() + "/data/states.json", "r", encoding="utf-8") as f:
    states_data = json.load(f)


def my_account(request):
    if request.method != "GET":
        return HttpResponse("Invalid method")
    elif request.user == "guest":
        return redirect("/signin")
    else:
        context = {
            "username": request.user.username,
            "cart_quantity": request.user.cart_quantity,
            "type": request.user.account_type
        }

    month_map = {
        '01': 'Jan',
        '02': 'Feb',
        '03': 'Mar',
        '04': 'Apr',
        '05': 'May',
        '06': 'Jun',
        '07': 'Jul',
        '08': 'Aug',
        '09': 'Sep',
        '10': 'Oct',
        '11': 'Nov',
        '12': 'Dec'
    }
    cards = []
    for card in request.user.cards.all():
        expiration_date = month_map[card.expiration_date[:2]
                                    ] + ' 20' + card.expiration_date[-2:]
        new_card = {
            'id': card.id,
            'card_type': card.card_type,
            'card_number': card.card_number[-4:],
            'expiration_date': expiration_date,
            'is_default': card.is_default
        }
        cards.append(new_card)

    context['name'] = request.user.name
    context['avatar'] = request.user.avatar
    context['addresses'] = request.user.addresses.all().values()
    context['cards'] = cards
    context['names'] = names_data
    context['phones'] = phones_data

    template = loader.get_template('my-account.html')
    return HttpResponse(template.render(context, request))


@csrf_exempt
def update(request, field):
    if request.method != "POST":
        return HttpResponse("Invalid method")
    elif request.user == "guest":
        return redirect("/signin")

    if field == "name":
        request.user.name = request.POST["name"]
        request.user.save()
    elif field == "password":
        if check_password(request.POST["old-password"], request.user.password):
            request.user.password = make_password(request.POST["new-password"])
            request.user.save()
        else:
            return HttpResponse('wrong password', content_type="text/plain")
    else:
        return HttpResponse("Invalid request")

    return redirect(request.META['HTTP_REFERER'])


@csrf_exempt
def get_states(request, country):
    if request.method != "POST":
        return HttpResponse("Invalid method")
    elif request.user == "guest":
        return redirect("/signin")

    return JsonResponse(states_data[country], safe=False)


@csrf_exempt
def address_add(request):
    if request.method != "POST":
        return HttpResponse("Invalid method")
    elif request.user == "guest":
        return redirect("/signin")

    user = request.user
    is_empty = False
    if not user.addresses.all():
        is_empty = True
    user.addresses.create(
        phone_number_code=request.POST['phone_number_code'],
        phone_number=request.POST['phone_number'],
        address=request.POST['address'],
        city=request.POST['city'],
        state=request.POST['state'],
        postal_code=request.POST['postal_code'],
        country=request.POST['country'],
        is_default=is_empty,
    )

    return redirect(request.META['HTTP_REFERER'])


@csrf_exempt
def address_set_default(request, address_id):
    if request.method != "POST":
        return HttpResponse("Invalid method")
    elif request.user == "guest":
        return redirect("/signin")

    user = request.user
    addresses = user.addresses.all()
    for address in addresses:
        if address.id != address_id:
            address.is_default = False
        else:
            address.is_default = True
        address.save()

    return redirect(request.META['HTTP_REFERER'])


@csrf_exempt
def address_remove(request, address_id):
    if request.method != "POST":
        return HttpResponse("Invalid method")
    elif request.user == "guest":
        return redirect("/signin")

    user = request.user
    address = user.addresses.all().get(id=address_id)
    address.delete()
    if address.is_default == True:
        addresses = User.objects.get(id=request.user.id).addresses.all()
        for _address in addresses:
            _address.is_default = True
            _address.save()
            break

    return redirect(request.META['HTTP_REFERER'])


@csrf_exempt
def card_add(request):
    if request.method != "POST":
        return HttpResponse("Invalid method")
    elif request.user == "guest":
        return redirect("/signin")

    user = request.user
    is_empty = False
    if not user.cards.all():
        is_empty = True
    user.cards.create(
        card_number=request.POST['card_number'].replace(' ', ''),
        cardholder_name=request.POST['cardholder_name'],
        expiration_date=request.POST['expiration_date'],
        card_type=request.POST['card_type'],
        cvc=request.POST['cvc'],
        is_default=is_empty,
    )

    return redirect(request.META['HTTP_REFERER'])


@csrf_exempt
def card_set_default(request, card_id):
    if request.method != "POST":
        return HttpResponse("Invalid method")
    elif request.user == "guest":
        return redirect("/signin")

    user = request.user
    cards = user.cards.all()
    for card in cards:
        if card.id != card_id:
            card.is_default = False
        else:
            card.is_default = True
        card.save()

    return redirect(request.META['HTTP_REFERER'])


@csrf_exempt
def card_remove(request, card_id):
    if request.method != "POST":
        return HttpResponse("Invalid method")
    elif request.user == "guest":
        return redirect("/signin")

    user = request.user
    card = user.cards.all().get(id=card_id)
    card.delete()
    if card.is_default == True:
        cards = User.objects.get(id=request.user.id).cards.all()
        for _card in cards:
            _card.is_default = True
            _card.save()
            break

    return redirect(request.META['HTTP_REFERER'])
