from django.shortcuts import render,redirect
from .form import signupForm, loginForm
from django.contrib.auth import authenticate,login
from django.contrib import messages

# Create your views here.

def home(request):
	return render(request,'authentication/home.html')

def about(request):
	return render(request,'authentication/about.html')

def signup(request):

	if request.method == "POST":
		userForm = signupForm(request.POST)
		
		if userForm.is_valid():
			userForm.save()
			return redirect('auth-home')
	else:
		userForm = signupForm(None)
	
	return render(request,'authentication/signup.html',{"form":userForm})

def LoginView(request):
	
	if request.method=="POST":
		form=loginForm(request.POST)
		username=request.POST['username']
		password=request.POST['password']
		user= authenticate(request,username=username, password=password)
		if user is not None:
			login(request,user)
			next_url = request.GET.get('next')
			if next_url:
				return redirect(next_url)
			return redirect('chat-userHome')
		else:
			form=loginForm(None)
			messages.error(request,'wrong username or password')
	else:
		form=loginForm(None)
	return render(request,'authentication/login.html',{"form":form})