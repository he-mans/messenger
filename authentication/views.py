from django.shortcuts import render,redirect
from .form import signupForm, loginForm
from django.contrib.auth import authenticate,login, logout
from django.contrib import messages
from django.views import generic
from django.urls import reverse_lazy


# Create your views here.

def home(request):
	if request.user.is_authenticated:
		return redirect('chat-userHome')
	return render(request,'authentication/home.html')


class signupView(generic.CreateView):
	template_name = 'authentication/signup.html'
	form_class = signupForm
	success_url = reverse_lazy('auth-home')

class LoginView(generic.View):
	form_class = loginForm
	template_name = "authentication/login.html"

	def verify_user(self):
		form=loginForm(self.request.POST)
		username, password = self.request.POST['username'], self.request.POST['password']
		user = authenticate(self.request,username=username, password=password)
		return (user,form)

	def post(self, *args, **kwargs):
		user,form= self.verify_user()
		if user is not None:
			login(self.request,user)
			return redirect(self.request.GET['next']) if self.request.GET.get('next',False) else redirect('chat-userHome')
		else:
			messages.error(self.request,'wrong username or password')
		return render(self.request,self.template_name,{"form":form})

	def get(self, *args, **kwargs):
		form=loginForm(None)
		return render(self.request,self.template_name,{"form":form})	

def LogoutView(request):
	if request.user.is_authenticated:
		logout(request)
	return redirect('auth-home')