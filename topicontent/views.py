from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
def _login(request):
    return HttpResponse("WEB-/login.html")