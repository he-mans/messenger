from django.shortcuts import render
from django.http import HttpResponse
from .userSignupForm import signup

# Create your views here.

def home(request):
	return render(request,'authentication/home.html')

def about(request):
	return render(request,'authentication/about.html')

def login(request):
	return render(request,'authentication/formHolder.html', )#{"form":signup})