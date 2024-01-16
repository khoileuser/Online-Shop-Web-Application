from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password

from web_app.models import User, Cart

from re import match
from secrets import token_urlsafe


@csrf_exempt
def sign_in(request):
    """
    The `sign_in` function handles the logic for user sign-in, checking if the user exists in the
    database and verifying their credentials.

    :param request: The `request` parameter is an object that represents the HTTP request made by the
    client. It contains information such as the request method (GET, POST, etc.), headers, user session,
    and any data sent with the request
    :return: The code is returning an HttpResponse object.
    """
    if request.method == "GET":
        if request.user == "guest":
            template = loader.get_template('authentication/sign-in.html')
            return HttpResponse(template.render())
        else:
            return redirect("/")
    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        try:
            user = User.objects.get(username=username)
            if check_password(password, user.password):
                return_session(request, user)
                if request.user.account_type == "A":
                    return redirect("/accounts")
                elif request.user.account_type == "S":
                    return redirect("/orders")
                elif request.user.account_type == "V":
                    return redirect("/products/vendor/" + request.user.username)
                return redirect("/")
            else:
                return HttpResponse("Invalid credentials")
        except:
            return HttpResponse("Cannot find this user in the database, have you signed?")


@csrf_exempt
def check_sign_in(request):
    """
    The function checks if a user's sign-in credentials are valid and returns "true" if they are, and
    "false" if they are not.

    :param request: The `request` parameter is an object that represents the HTTP request made by the
    client. It contains information such as the request method (e.g., GET, POST), headers, cookies, and
    the request body
    :return: an HttpResponse object. The content of the HttpResponse object depends on the conditions
    met in the code. If the username and password are correct, it returns "true". If the username or
    password is incorrect, it returns "false".
    """
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        try:
            user = User.objects.get(username=username)
            if check_password(password, user.password):
                return_session(request, user)
                return HttpResponse("true")
            else:
                return HttpResponse("false")
        except:
            return HttpResponse("false")


@csrf_exempt
def sign_up(request):
    """
    The `sign_up` function handles the sign-up process for a user, validating their input and creating a
    new user account if the input is valid.

    :param request: The `request` parameter is an object that represents the HTTP request made by the
    client. It contains information such as the request method (GET or POST), the user making the
    request, and any data sent with the request (e.g., form data)
    :return: an HTTP response.
    """
    if request.method == "GET":
        if request.user == "guest":
            template = loader.get_template('authentication/sign-up.html')
            return HttpResponse(template.render())
        else:
            return redirect("/")
    elif request.method == "POST":
        name = request.POST["name"]
        if len(name) > 255 or len(name) == 0:
            return HttpResponse("Name must be lower than 255 characters and not empty.")

        username = request.POST["username"]
        if len(username) < 4 or len(username) > 25 or match(r'^[a-zA-Z0-9]+$', username) is None:
            return HttpResponse("Usernames must contain only letters and digits and between 4 and 25 characters.")

        password = request.POST["password"]
        if match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,4096}$', password) is None:
            return HttpResponse("Passwords must contain at least one uppercase, one lowercase, one digit, one special character and at least 8 characters long.")
        hashed_pwd = make_password(password)

        match request.POST["accounttype"]:
            case "customer":
                account_type = "C"
            case "shipper":
                account_type = "S"
            case "vendor":
                account_type = "V"
            # case "admin":
            #     account_type = "A"

        try:
            user = User(name=name, username=username, password=hashed_pwd,
                        account_type=account_type, avatar=None, share_wishlist=False)
        except:
            return HttpResponse("Invalid credentials")
        user.save()

        Cart.objects.create(owner=user)

        return_session(request, user)
        if user.account_type == "A":
            return redirect("/accounts")
        elif user.account_type == "S":
            return redirect("/orders")
        elif user.account_type == "V":
            return redirect("/products/vendor/" + user.username)
        return redirect("/")


@csrf_exempt
def check_sign_up(request):
    """
    The function checks if a username already exists in the User model and returns "true" if it does,
    and "false" if it doesn't.

    :param request: The `request` parameter is an object that represents the HTTP request made by the
    client. It contains information such as the request method (e.g., GET or POST), the request headers,
    and the request data
    :return: an HttpResponse object. The content of the HttpResponse object depends on the conditions in
    the code. If a user with the given username already exists, it will return "true". If a user with
    the given username does not exist, it will return "false". If there is an exception during the
    process, it will also return "false".
    """
    if request.method == "POST":
        username = request.POST["username"]
        try:
            user = User.objects.get(username=username)
            if user:
                return HttpResponse("true")
            else:
                return HttpResponse("false")
        except:
            return HttpResponse("false")


def token_generator():
    """
    The function `token_generator` generates a random URL-safe token of length 32.
    :return: a randomly generated token of length 32.
    """
    return token_urlsafe(32)


def return_session(request, user):
    """
    The function sets the user ID and generates a token for the user's session, and then adds the token
    to the user's list of tokens.

    :param request: The "request" parameter is an object that represents the HTTP request made by the
    client. It contains information about the request, such as the headers, body, and session data
    :param user: The "user" parameter is an instance of a user model. It represents the user for whom
    the session is being created or updated
    """
    request.session["user_id"] = user.id
    generated_token = token_generator()
    request.session["token"] = generated_token
    if user.tokens is None:
        user.tokens = [generated_token]
    else:
        user.tokens.append(generated_token)
    user.save()


def sign_out(request):
    """
    The `sign_out` function removes the token associated with the user from the session and redirects
    the user to the homepage.

    :param request: The `request` parameter is an object that represents the HTTP request made by the
    user. It contains information about the request, such as the user making the request, the session
    data, and any data sent in the request body or query parameters
    :return: a redirect to the homepage ("/").
    """
    if request.user != 'guest':
        requested_token = request.session.get("token")
        request.user.tokens.remove(requested_token)
        request.user.save()

        fields = ["user_id", "token"]
        for field in fields:
            try:
                del request.session[field]
            except KeyError:
                continue
    return redirect("/")


def view_accounts(request):
    """
    The `view_accounts` function returns a list of all the users in the database.

    :param request: The `request` parameter is an object that represents the HTTP request made by the
    user. It contains information about the request, such as the user making the request, the session
    data, and any data sent in the request body or query parameters
    :return: a list of all the users in the database.
    """
    if request.method == "GET" and request.user.account_type == "A":
        context = {
            "username": request.user.username,
            "type": request.user.account_type,
            "users": User.objects.all().order_by("id")
        }

        template = loader.get_template('authentication/accounts.html')
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponse("You are not an admin.")


@csrf_exempt
def update_account(request, account_id):
    """
    The `update_account` function updates the user's account information.

    :param request: The `request` parameter is an object that represents the HTTP request made by the
    user. It contains information about the request, such as the user making the request, the session
    data, and any data sent in the request body or query parameters
    :return: a redirect to the accounts ("/accounts").
    """
    if request.method == "POST" and request.user.account_type == "A":
        username = request.POST["username-" + str(account_id)]
        if len(username) < 4 or len(username) > 25 or match(r'^[a-zA-Z0-9]+$', username) is None:
            return HttpResponse("Usernames must contain only letters and digits and between 4 and 25 characters.")

        password = request.POST["password-" + str(account_id)]
        if password != "":
            if match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,4096}$', password) is None:
                return HttpResponse("Passwords must contain at least one uppercase, one lowercase, one digit, one special character and at least 8 characters long.")
            hashed_pwd = make_password(password)

        match request.POST["accounttype-" + str(account_id)]:
            case "customer":
                account_type = "C"
            case "shipper":
                account_type = "S"
            case "vendor":
                account_type = "V"

        try:
            user = User.objects.get(id=account_id)
            user.username = username
            if password != "":
                user.password = hashed_pwd
            user.account_type = account_type
            user.save()
        except:
            return HttpResponse("User not found.")

        return redirect("/accounts")
    else:
        return HttpResponse("You are not an admin.")


@csrf_exempt
def delete_account(request, account_id):
    """
    The `delete_account` function deletes a user's account along with their associated cards, addresses,
    products in their cart, and session data, and then redirects to the homepage.

    :param request: The `request` parameter is an object that represents the HTTP request made by the
    user. It contains information about the request, such as the user making the request, the session
    data, and any data sent in the request body or query parameters
    :param account_id: The `account_id` parameter is the ID of the user whose account is being deleted
    :return: a redirect to the accounts ("/accounts").
    """
    if request.method == "POST" and request.user.account_type == "A":
        try:
            user = User.objects.get(id=account_id)
        except:
            return HttpResponse("User not found.")

        cards = user.cards.all()
        for card in cards:
            card.delete()

        addresses = user.addresses.all()
        for address in addresses:
            address.delete()

        cart = Cart.objects.get(owner=user)
        for product in cart.products.all():
            product.delete()

        user.delete()

        return redirect("/accounts")
    else:
        return HttpResponse("You are not an admin.")
