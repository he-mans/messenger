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

class LoginView(generic.edit.FormView):
    form_class = loginForm
    template_name = "authentication/login.html"
    success_url = reverse_lazy('chat-userHome')

    def get_success_url(self):
         if self.request.GET.get('next',False):
            return self.request.GET['next']
         else:
            return LoginView.success_url

    def form_valid(self,form):
        username,password = form.cleaned_data['username'],form.cleaned_data['password']
        print(username,password)
        user = authenticate(self.request,username=username,password=password)
        if user is not None:
            login(self.request,user)
            self.success_url = self.get_success_url()
            return super().form_valid(form)
        else:
            messages.error(self.request,'wrong username or password')
            return render(self.request,self.template_name,{"form":form})

def LogoutView(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('auth-home')