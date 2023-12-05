from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


def checkout_(request):
    template = loader.get_template("checkout.html")
    return HttpResponse(template.render())
