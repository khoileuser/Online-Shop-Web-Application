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

    # my account
    path('my-account/', views.my_account),
    path('me/', views.my_account),

    # check authentication
    path('check/signin/', authentication.check_sign_in),
    path('check/signup/', authentication.check_sign_up),

    # cart
    path('cart/', cart.view_cart),
    path('cart/add/<int:product_id>/quantity/<int:quantity>', cart.add_to_cart),
    path('cart/remove/<int:product_id>/quantity/<str:quantity>',
         cart.remove_from_cart),

    # order
    path('checkout/', order.checkout),
    path('place_order/', order.place_order),
    path('order/<int:order_id>', order.view_order),
    path('orders/<int:order_id>', order.view_order),
    path('orders/', order.view_orders),

    # product
    path('products/', products.listing),
    path('products/<int:product_id>', products.product),
    path('product/<int:product_id>', products.product),

    # testing
    path('execute/', views.execute),
]
