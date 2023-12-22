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

    # check authentication
    path('check/signin/', authentication.check_sign_in),
    path('check/signup/', authentication.check_sign_up),

    # cart
    path('cart/', cart.view_cart),
    path('cart/add/<int:product_id>/quantity/<int:quantity>', cart.add_to_cart),
    path('cart/remove/<int:product_id>/quantity/<str:quantity>',
         cart.remove_from_cart),
    path('checkout/', cart.checkout),

    # product
    path('products/', products.listing),
    path('products/<int:product_id>', products.product),
    path('product/<int:product_id>', products.product),

    # testing
    path('execute/', views.execute),
]
