from django.urls import path
from .views import *

urlpatterns = [
    path('', views.index),
    path('signin/', authentication.sign_in),
    path('signup/', authentication.sign_up),
    path('signout/', authentication.sign_out),
    path('product/', product.product_),
]
