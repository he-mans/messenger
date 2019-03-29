from django.shortcuts import render
from django.views import generic
from .models import Contacts, Messages
from django.contrib.auth.models import User
from django.http import JsonResponse
import json
from django.db.models import Q
# Create your views here.

def createContact(contact_user,contact_contact):
    user = User.objects.filter(username=contact_user).first()
    contact = User.objects.filter(username=contact_contact).first()
    contact_receiver_to_sender = Contacts(user=user,contact=contact)
    contact_sender_to_receiver = Contacts(user=contact,contact=user)
    contact_receiver_to_sender.save()
    contact_sender_to_receiver.save()
    return(contact_receiver_to_sender)

def getContact():
    pass

def SaveMessageView(request):
    contact_user = request.POST.get('receiver')
    contact_contact = request.POST.get('sender')
    contacts = Contacts.objects.filter(user__username=contact_user,contact__username=contact_contact)
    
    if not (len(contacts)):
        contact_r2s= createContact(contact_user,contact_contact)
    else:
        contact_r2s=contacts[0]
    
    messageReceived = request.POST.get('message')
    if messageReceived != "":
        message = Messages(related_contact=contact_r2s,message = messageReceived)
        message.save(overrideSave=True,)
    return JsonResponse({"saved":"true"})


def getContactsDetail(request):
    contacts = Contacts.objects.filter(user=request.user).all()
    contacts = contacts.order_by('-last_message__date_created')
    return contacts

def GetMessagesView(request):
    user,sender = request.GET.get('user'),request.GET.get('receiver')
    messages_all = Messages.objects.filter( Q(related_contact__user__username=user)&Q(related_contact__contact__username=sender)
                                                                            |  
                                                Q(related_contact__user__username=sender)&Q(related_contact__contact__username=user)  ) 

    messages = list(messages_all.order_by('date_created').values('message','related_contact__contact__username','date_created'))
    
    for message in messages_all.filter( Q(related_contact__user__username=user)&
                                        Q(related_contact__contact__username=sender)&
                                        Q(read=False) ):
        message.read=True
        contact=message.related_contact
        contact.unread_messages-=1
        try:
            contact.full_clean()
            contact.save()
        except:
            pass
        message.save(overrideSave=False)
    return JsonResponse({"messages":messages})

def GetProfilePicture(data):
    username = data.GET.get('username')
    profilePic = User.objects.filter(username=username).first()
    profilePic = profilePic.profile.profile_picture.url
    print("sadfsdfsafasdfasdfasdfasdfasdfsd\n\n\n")
    return JsonResponse({"profile_picture":profilePic})

def getNotification(user):
    notifications = Contacts.objects.filter( 
                                            Q(user__username=user)
                                            &~Q(unread_messages=0)
                                            &Q(last_message__delivered=False) 
                                            ).order_by('last_message__date_created'
                                            ).values  ('contact__username','unread_messages',
                                                       'last_message__message',
                                                      )
    return list(notifications)

def CheckMessagesView(request):
    user = request.GET.get('user')
    current_chat_window = request.GET.get('currentChatWindow')
    undelivered_messages = None

    #getting all undelivered messages
    undelivered_messages_all = Messages.objects.filter( Q(related_contact__user__username=user)&Q(delivered=False) )

    if current_chat_window!='':
        #getting only currnet chat window use messages
        undelivered_messages = undelivered_messages_all.filter(related_contact__contact__username=current_chat_window)
        undelivered_messages.read=True
        undelivered_messages.delivered=True
        for message in undelivered_messages:
            contact = message.related_contact
            contact.unread_messages-=1
            try:
                contact.full_clean()
                contact.save()
            except:
                pass
            message.save(overrideSave=False)
        undelivered_messages =list(undelivered_messages.values('message','related_contact__contact__username'))

    #notification for all other messages
    notifications = getNotification(user)
    
    undelivered_messages_all.update(delivered=True)
    for messages in undelivered_messages_all:
        messages.save(overrideSave=False)
    
    return JsonResponse({"messages":undelivered_messages,"notifications":notifications})