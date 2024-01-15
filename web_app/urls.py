from django.urls import path
from .views import *

urlpatterns = [
    path('', views.index),
    path('about/', views.about),
    path('terms/', views.terms),
    path('privacy/', views.privacy),

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
    path('my-account/', me.my_account),
    path('me/', me.my_account),
    path('me/update/<str:field>', me.update_account),
    path('me/delete/', me.delete_account),
    path('me/address/add/', me.address_add),
    path('me/address/set/default/<int:address_id>', me.address_set_default),
    path('me/address/remove/<int:address_id>', me.address_remove),
    path('me/card/add/', me.card_add),
    path('me/card/set/default/<int:card_id>', me.card_set_default),
    path('me/card/remove/<int:card_id>', me.card_remove),
    path('states/get/<str:country>', me.get_states),

    # wishlist
    path('wishlist/<str:username>', wishlist.view_wishlist),
    path('wishlist/add/<int:product_id>', wishlist.add_to_wishlist),
    path('wishlist/remove/<int:product_id>', wishlist.remove_from_wishlist),
    path('wishlist/share/<str:value>', wishlist.share_toggle),

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
    path('checkout/change/<str:field>', order.checkout_change),
    path('order/place/', order.place_order),
    path('order/<int:order_id>', order.view_order),
    path('order/<int:order_id>/status/<str:status>', order.set_order_status),
    path('orders/<int:order_id>', order.view_order),
    path('orders/', order.view_orders),

    # product
    path('products/', product.listing),
    path('products/vendor/<str:vendor>', product.listing_vendor),
    path('products/<int:product_id>', product.view_product),
    path('product/<int:product_id>', product.view_product),
    path('product/add/', product.add_product),
    path('product/update/<int:product_id>', product.update_product),
    path('product/delete/<int:product_id>', product.delete_product),
    path('product/review/<int:product_id>', product.add_review),

    # admin
    path('accounts/', authentication.view_accounts),
    path('account/update/<int:account_id>', authentication.update_account),
    path('account/delete/<int:account_id>', authentication.delete_account),

    # testing
    path('execute/', views.execute),
]
