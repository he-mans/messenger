from django.urls import path
from . import views

urlpatterns=[
	path('scout/<slug:username>/',views.ProfileView.as_view(), name='chat-profile'),
	path('',views.userHome, name='chat-userHome'),
	path('profile/',views.ProfileSettings.as_view(),name='chat-profile-settings')
]
