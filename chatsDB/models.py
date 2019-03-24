from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
# Create your models here.

class Messages(models.Model):
	sender = models.ForeignKey(User,on_delete=models.PROTECT, related_name="sender")
	receiver = models.ForeignKey(User, on_delete=models.PROTECT, related_name="receiver")
	message = models.TextField(null=False ,blank=False)
	date_created=models.DateTimeField(auto_now = True)
	read = models.BooleanField(default=False)

	def __str__(self):
		return f'from {self.sender.username} to {self.receiver.username} || message:{self.message}'

	def save(self,*args,**kwargs):
		if not self.receiverConnected():
			self.addReceiverToContacts()
		super().save(*args,**kwargs)
		self.updateLastMessage()
	
	def receiverConnected(self):
		sender_contact_list = self.sender.contacts.all()
		sender_contact_list = sender_contact_list.filter(contact=self.receiver)
		return True if len(sender_contact_list) > 0 else False

	def addReceiverToContacts(self):
		contact = Contacts(user=self.sender, contact=self.receiver)
		contact.save()

	def updateLastMessage(self):
		contact = Contacts.objects.filter(Q(user=self.sender)&Q(contact=self.receiver)).first()
		contact.last_message=self
		contact.unread_messages+=1
		contact.save()


class Contacts(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contacts")
	contact = models.ForeignKey(User,on_delete=models.CASCADE, related_name="list")
	last_message = models.ForeignKey(Messages, null=True,on_delete=models.SET_NULL)
	unread_messages = models.PositiveIntegerField(null=False, default=0)

	def __str__(self):
		if self.contact==None:
			return f'{self.user.username} has no connections'	
		return f"{self.user.username} connected with {self.contact.username}"
