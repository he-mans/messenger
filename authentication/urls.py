from django.urls import path
from . import views

urlpatterns = [
	path('',views.home,name='auth-home'),
	path('signup/',views.signup, name='auth-signup'),
	path('login/',views.LoginView, name='auth-login')
]