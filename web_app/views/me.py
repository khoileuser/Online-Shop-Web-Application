from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from django.forms.models import model_to_dict
from django.core.files.storage import FileSystemStorage

from web_app.models import User, Cart
from web_app.data import *

from os import remove, getcwd

fs = FileSystemStorage()


def my_account(request):
    """
    The `my_account` function retrieves user account information and renders it in a template for
    display.

    :param request: The `request` parameter is an object that represents the HTTP request made by the
    client. It contains information such as the request method (GET, POST, etc.), user information, and
    any data sent with the request
    :return: an HttpResponse object.
    """
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

    template = loader.get_template('me/my-account.html')
    return HttpResponse(template.render(context, request))


@csrf_exempt
def delete_account(request):
    """
    The `delete_account` function deletes a user's account along with their associated cards, addresses,
    products in their cart, and session data, and then redirects to the homepage.

    :param request: The "request" parameter is an object that represents the HTTP request made by the
    client. It contains information about the request, such as the method used (GET, POST, etc.), user
    information, session data, and more. In this case, the function is expecting a request object to be
    passed
    :return: a redirect to the root URL ("/").
    """
    if request.method != "POST":
        return HttpResponse("Invalid method")
    elif request.user == "guest":
        return redirect("/signin")

    cards = request.user.cards.all()
    for card in cards:
        card.delete()

    addresses = request.user.addresses.all()
    for address in addresses:
        address.delete()

    cart = Cart.objects.get(owner=request.user)
    for product in cart.products.all():
        product.delete()

    request.user.delete()

    fields = ["user_id", "token"]
    for field in fields:
        try:
            del request.session[field]
        except KeyError:
            continue

    return redirect("/")


@csrf_exempt
def update_account(request, field):
    """
    The function updates the name or password of a user based on the request and field provided.

    :param request: The `request` parameter is an object that represents the HTTP request made by the
    client. It contains information such as the request method (GET, POST, etc.), user information, and
    any data sent with the request
    :param field: The "field" parameter is used to determine which field of the user object needs to be
    updated. It can have two possible values: "name" or "password"
    :return: a redirect response to the previous page (referenced by `request.META['HTTP_REFERER']`)
    after updating the specified field in the user object.
    """
    if request.method != "POST":
        return HttpResponse("Invalid method")
    elif request.user == "guest":
        return redirect("/signin")

    # Update user name
    if field == "name":
        request.user.name = request.POST["name"]
        request.user.save()

    # Update user password
    elif field == "password":
        if check_password(request.POST["old-password"], request.user.password):
            request.user.password = make_password(request.POST["new-password"])
            request.user.save()
        else:
            return HttpResponse('wrong password', content_type="text/plain")

    # Update user avatar
    elif field == "avatar":
        try:
            avatar = request.FILES['avatar']
            if request.user.avatar:
                remove(getcwd() + '/web_app/static/images/avatar/' +
                       request.user.avatar)
            fs.save(getcwd() + '/web_app/static/images/avatar/' +
                    avatar.name, avatar)
            request.user.avatar = avatar.name
        except:
            if request.user.avatar:
                remove(getcwd() + '/web_app/static/images/avatar/' +
                       request.user.avatar)
            request.user.avatar = None
        request.user.save()
    else:
        return HttpResponse("Invalid request")

    return redirect(request.META['HTTP_REFERER'])


@csrf_exempt
def get_states(request, country):
    """
    The function `get_states` returns a JSON response containing the states data for a given country,
    but only if the request method is POST and the user is not a guest.

    :param request: The `request` parameter is an object that represents the HTTP request made by the
    client. It contains information such as the HTTP method used (e.g., GET, POST), user authentication
    details, and any data sent with the request
    :param country: The country parameter is the name of the country for which you want to retrieve the
    states
    :return: a JSON response containing the states data for the specified country.
    """
    if request.method != "POST":
        return HttpResponse("Invalid method")
    elif request.user == "guest":
        return redirect("/signin")

    return JsonResponse(states_data[country], safe=False)


@csrf_exempt
def address_add(request):
    """
    The function `address_add` adds a new address to a user's profile if the request method is POST and
    the user is not a guest.

    :param request: The `request` parameter is an object that represents the HTTP request made by the
    client. It contains information such as the HTTP method used (GET, POST, etc.), user information,
    and data sent in the request
    :return: a redirect to the previous page (HTTP_REFERER) after adding an address to the user's
    addresses.
    """
    if request.method != "POST":
        return HttpResponse("Invalid method")
    elif request.user == "guest":
        return redirect("/signin")

    user = request.user
    is_empty = False
    if not user.addresses.all():
        is_empty = True
    address = user.addresses.create(
        phone_number_code=request.POST['phone_number_code'],
        phone_number=request.POST['phone_number'],
        address=request.POST['address'],
        city=request.POST['city'],
        state=request.POST['state'],
        postal_code=request.POST['postal_code'],
        country=request.POST['country'],
        is_default=is_empty,
    )

    path = request.META.get('HTTP_REFERER')
    if '/checkout/' in path:
        context = request.session.get("context")
        context["address"] = model_to_dict(address)
        request.session["context"] = context
        return redirect('/checkout/')
    elif '/my-account/' in path or '/me/' in path:
        return redirect(request.META['HTTP_REFERER'])


@csrf_exempt
def address_set_default(request, address_id):
    """
    The function sets a specific address as the default address for a user and redirects to the previous
    page.

    :param request: The `request` parameter is an object that represents the HTTP request made by the
    client. It contains information such as the method used (GET, POST, etc.), user information, and
    other metadata
    :param address_id: The `address_id` parameter is the ID of the address that the user wants to set as
    the default address
    :return: a redirect to the previous page (the referer) in the request's META data.
    """
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
    """
    The function `address_remove` removes a user's address and sets a new default address if the deleted
    address was the previous default.

    :param request: The `request` parameter is an object that represents the HTTP request made by the
    client. It contains information such as the request method (GET, POST, etc.), user information, and
    other data related to the request
    :param address_id: The `address_id` parameter is the unique identifier of the address that needs to
    be removed
    :return: a redirect to the previous page (HTTP_REFERER) after deleting an address.
    """
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
    """
    The `card_add` function adds a new card to a user's account if the request method is POST and the
    user is authenticated, otherwise it redirects to the sign-in page.

    :param request: The `request` parameter is an object that represents the HTTP request made by the
    client. It contains information such as the request method (e.g., GET, POST), user information, and
    data sent in the request
    :return: a redirect to the previous page (the referer page) after adding a card to the user's
    account.
    """
    if request.method != "POST":
        return HttpResponse("Invalid method")
    elif request.user == "guest":
        return redirect("/signin")

    user = request.user
    is_empty = False
    if not user.cards.all():
        is_empty = True
    card = user.cards.create(
        card_number=request.POST['card_number'].replace(' ', ''),
        cardholder_name=request.POST['cardholder_name'],
        expiration_date=request.POST['expiration_date'],
        card_type=request.POST['card_type'],
        cvc=request.POST['cvc'],
        is_default=is_empty,
    )

    path = request.META.get('HTTP_REFERER')
    if '/checkout/' in path:
        context = request.session.get("context")
        expiration_date = month_map[card.expiration_date[:2]
                                    ] + ' 20' + card.expiration_date[-2:]
        context["card"] = {
            'id': card.id,
            'card_type': card.card_type,
            'card_number': card.card_number[-4:],
            'expiration_date': expiration_date,
            'is_default': card.is_default
        }
        request.session["context"] = context
        return redirect('/checkout/')
    elif '/my-account/' in path or '/me/' in path:
        return redirect(request.META['HTTP_REFERER'])


@csrf_exempt
def card_set_default(request, card_id):
    """
    The function sets a specific card as the default card for a user and redirects the user to the
    previous page.

    :param request: The `request` parameter is an object that represents the HTTP request made by the
    client. It contains information such as the method used (GET, POST, etc.), user information, and
    other metadata
    :param card_id: The `card_id` parameter is the ID of the card that the user wants to set as the
    default card
    :return: a redirect to the previous page (request.META['HTTP_REFERER']) after setting the
    "is_default" attribute of the specified card to True and all other cards to False.
    """
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
    """
    The `card_remove` function removes a card from a user's account and sets a new default card if the
    removed card was the previous default.

    :param request: The `request` parameter is an object that represents the HTTP request made by the
    client. It contains information such as the request method (e.g., GET, POST), user information, and
    other metadata
    :param card_id: The `card_id` parameter is the unique identifier of the card that needs to be
    removed
    :return: a redirect to the previous page (the referer) after deleting a card.
    """
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
