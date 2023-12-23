from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from web_app.models import Product

def listing(request):
    template = loader.get_template("listing.html")
    return HttpResponse(template.render())

def listing_2(request):
    template = loader.get_template("listing_2.html")
    return HttpResponse(template.render())
