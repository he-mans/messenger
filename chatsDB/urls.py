from django.urls import path
from . import views

urlpatterns=[
	path('send/',views.SaveMessageView,name='chatsDB-send'),
	path('get/',views.GetMessagesView,name='chatsDB-get'),
	path('check/',views.CheckMessagesView, name='chatsDB-check'),
	path('getdp/',views.GetProfilePicture,name='chatsDB-get-dp')
]