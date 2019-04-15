from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.validators import MinValueValidator
# Create your models here.

class Messages(models.Model):
	related_contact = models.ForeignKey('Contacts', on_delete=models.CASCADE, related_name="messages")
	message = models.TextField(null=False ,blank=False)
	date_created=models.DateTimeField(auto_now = True)
	read = models.BooleanField(default=False)
	delivered = models.BooleanField(default=False)

	class Meta:
		verbose_name="messages"

	def __str__(self):
		return f'from {self.related_contact.contact.username} to {self.related_contact.user.username} || message:{self.message}'

	def save(self,overrideSave=True,*args,**kwargs):
		super().save(*args,**kwargs)
		if overrideSave:
			self.updateLastMessage()

	def updateLastMessage(self):
		receiver=self.related_contact.user
		reverse_contact = self.related_contact.contact.contacts.filter(contact=receiver).first()
		reverse_contact.last_message=self
		self.related_contact.last_message=self
		self.related_contact.unread_messages+=1
		self.related_contact.save()
		reverse_contact.save()

class Contacts(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contacts")
	contact = models.ForeignKey(User,on_delete=models.CASCADE, related_name="inContactList")
	last_message = models.ForeignKey(Messages, null=True,blank=True,on_delete=models.SET_NULL)
	unread_messages = models.PositiveIntegerField(null=False, default=0, validators=[MinValueValidator(0)])

	def __str__(self):
		if self.contact==None:
			return f'{self.user.username} has no connections'	
		return f"{self.user.username} connected with {self.contact.username}"

