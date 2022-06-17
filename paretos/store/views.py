from django.shortcuts import render
from .models import *


def say_hello(request):
    return render(request, "home.html", context={})
