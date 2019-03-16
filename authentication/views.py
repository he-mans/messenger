from django.shortcuts import render,redirect
from .form import signupForm, loginForm
from django.contrib.auth import authenticate,login


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
			return redirect('auth-home')
	else:
		form=loginForm(None)
	return render(request,'authentication/login.html',{"form":loginForm})