from django.shortcuts import render
from django.http import HttpResponse

def indexPage(request):
    return HttpResponse('hello polls')
