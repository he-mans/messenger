from django.urls import path
from . import views

urlpatterns = [
	path('',views.home,name='auth-home'),
	path('signup/',views.login, name='auth-signup')
]