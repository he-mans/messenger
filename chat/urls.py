from django.urls import path
from . import views

urlpatterns=[
	path('<slug:username>/',views.profile, name='chat-profile'),
	path('',views.userHome, name='chat-userHome')
]
