from django.http import HttpResponse
from django.shortcuts import render

def index2(request):
    return HttpResponse("Hello world")


def index(request):
    return render(request, 'index.html', {})
