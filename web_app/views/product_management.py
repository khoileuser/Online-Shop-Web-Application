from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


def create_product(request):
    if request.method == "GET":
        template = loader.get_template(
            'product-management/create-product.html')
        return HttpResponse(template.render())
