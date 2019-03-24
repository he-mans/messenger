from django.urls import path
from . import views

urlpatterns=[
	path('scout/<slug:username>/',views.ProfileView.as_view(), name='chat-profile'),
	path('',views.UserHome.as_view(), name='chat-userHome'),
	path('profile/',views.ProfileSettings.as_view(),name='chat-profile-settings'),
	path('search_user/',views.SearchUser,name='chat-search-user')
]
