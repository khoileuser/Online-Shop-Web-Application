from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


def my_account(request):
    template = loader.get_template('account/my-account.html')
    return HttpResponse(template.render())
