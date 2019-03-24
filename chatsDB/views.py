from django.shortcuts import render
from django.views import generic
from .models import Contacts, Messages
from django.contrib.auth.models import User
from django.http import JsonResponse
import json

# Create your views here.

def SaveMessageView(request):
	message_ = Messages()
	sender = User.objects.filter(username=request.POST.get('sender')).first()
	message_.sender = sender
	receiver = User.objects.filter(username=request.POST.get('receiver')).first()
	message_.receiver = receiver
	messageReceived = request.POST.get('message')
	if messageReceived != "":
		message_.message = request.POST.get('message')
		message_.save()
	return JsonResponse({"saved":"true"})

def getContactsDetail(request):
	contacts = Contacts.objects.filter(user=request.user).all()
	return contacts

