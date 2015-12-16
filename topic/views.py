from django.shortcuts import render
from django.template.response import TemplateResponse
from django.http import HttpResponse, HttpResponseRedirect

def index(request):
    return TemplateResponse(request, 'index.html')

def login(request):
    return TelatempResponse(request, "WEB-/login.html")