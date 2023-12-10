from django.urls import path
from .views import *

urlpatterns = [
    path('', views.index),

    # authentication
    path('signin/', authentication.sign_in),
    path('sign-in/', authentication.sign_in),
    path('login/', authentication.sign_in),
    path('log-in/', authentication.sign_in),
    path('signup/', authentication.sign_up),
    path('sign-up/', authentication.sign_up),
    path('signout/', authentication.sign_out),
    path('sign-out/', authentication.sign_out),
    path('logout/', authentication.sign_out),
    path('log-out/', authentication.sign_out),

    # consumer
    path('cart/', cart.cart_),
    path('addtocart/<int:id>/<int:quantity>', cart.add_to_cart),
    path('add-to-cart/<int:id>/<int:quantity>', cart.add_to_cart),

    path('execute/', views.execute),
]
