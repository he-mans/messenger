from django.urls import path
from . import views


urlpatterns = [
	path('',views.home,name='auth-home'),
	path('signup/',views.signupView.as_view(), name='auth-signup'),
	path('login/',views.LoginView.as_view(), name='auth-login'),
	path('logout/',views.LogoutView, name='auth-logout')
]