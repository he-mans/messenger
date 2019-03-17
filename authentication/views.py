from django.shortcuts import render,redirect
from .form import signupForm, loginForm
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.views import generic
from django.urls import reverse_lazy


# Create your views here.

def home(request):
	return render(request,'authentication/home.html')

def about(request):
	return render(request,'authentication/about.html')

class signupView(generic.CreateView):
	template_name = 'authentication/signup.html'
	form_class = signupForm
	success_url = reverse_lazy('auth-home')


def LoginView(request):
	if request.method=="POST":
		form=loginForm(request.POST)
		username, password = request.POST['username'], request.POST['password']
		user = authenticate(request,username=username, password=password)
		if user is not None:
			login(request,user)
			next_url = request.GET.get('next')
			if next_url:
				return redirect(next_url)
			return redirect('chat-userHome')
		else:
			messages.error(request,'wrong username or password')
	else:
		form=loginForm(None)
	return render(request,'authentication/login.html',{"form":form})	