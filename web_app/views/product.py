from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


def product_(request):
    template = loader.get_template("product.html")
    
    return HttpResponse(template.render())
