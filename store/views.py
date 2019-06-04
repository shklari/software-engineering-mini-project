from django.http import HttpResponse
from django.shortcuts import render

from . import models

#create your views here


def index(request):
    return render(request, 'store/home.html')
