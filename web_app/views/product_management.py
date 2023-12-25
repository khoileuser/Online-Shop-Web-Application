from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


def add_product(request):
    template = loader.get_template("product-management/addproduct.html")
    return HttpResponse(template.render())

def update_product(request):
    template = loader.get_template("product-management/updateproduct.html")
    return HttpResponse(template.render())