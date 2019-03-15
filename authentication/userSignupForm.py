from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class signup(forms.ModelForm):
	username=forms.CharField(label='')
	password= forms.CharField(widget=forms.PasswordInput, label='')
	email=forms.EmailField(label='')

	class Meta:
		model=User
		fields= ['username','email','password']

	def __init__(self,*args,**kwargs):
		super(signup, self).__init__(*args,**kwargs)
		self.fields['password'].widget.attrs.update({
				"placeholder":"password",
			})

		self.fields['email'].widget.attrs.update({
				"placeholder":"email"
			})

		self.fields['username'].widget.attrs.update({
				"placeholder":"username"
			})