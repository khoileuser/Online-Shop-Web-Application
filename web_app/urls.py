from django.urls import path
from .views import *

print(product_management)

urlpatterns = [
    path('', views.index),
    path('signin/', authentication.sign_in),
    path('signup/', authentication.sign_up),
    path('signout/', authentication.sign_out),
    path('create-product/', product_management.create_product),
]
