from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class signupForm(UserCreationForm):
	password1= forms.CharField(widget=forms.PasswordInput, label='')
	password2= forms.CharField(widget=forms.PasswordInput, label='')
	email=forms.EmailField(label='')
	username=forms.CharField(label='')

	class Meta:
		model=User
		fields= ['username','email','password1']

	def __init__(self,*args,**kwargs):
		super(signupForm, self).__init__(*args,**kwargs)
		self.fields['password1'].widget.attrs.update({
				"placeholder":"password",
			})

		self.fields['password2'].widget.attrs.update({
				"placeholder":"confirm password",
			})

		self.fields['email'].widget.attrs.update({
				"placeholder":"email"
			})

		self.fields['username'].widget.attrs.update({
				"placeholder":"username"
			})

class loginForm(forms.ModelForm):
	password=forms.CharField(widget=forms.PasswordInput,label='')
	username=forms.CharField(label='')

	class Meta:
		model=User
		fields=['username','password']

	def __init__(self,*args,**kwargs):
		super(loginForm,self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs.update({
				"placeholder":"username"
			})
		self.fields['password'].widget.attrs.update({
				"placeholder":"password"
			})