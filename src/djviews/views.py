from django.http import HttpResponse
from django.shortcuts import render

# def home(request):
#     print(dir(request))
#     return HttpResponse("<h1> Hello world! </h1>")

def home(request):
    return HttpResponse("Hello World!")