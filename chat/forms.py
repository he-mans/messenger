from django import forms
from django.contrib.auth.models import User
from .models import Profile

class ProfileUpdateForm(forms.ModelForm):
    status = forms.CharField(label='')
    profile_picture = forms.ImageField(widget=forms.FileInput, label='')
    
    class Meta:
        model=Profile
        fields=['status', 'profile_picture']

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm,self).__init__(*args,**kwargs)
        self.fields['status'].widget.attrs.update({
                "placeholder":"status"
            })

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label='')
    username = forms.CharField(label='')

    class Meta:
        model=User
        fields=['username','email']

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm,self).__init__(*args,**kwargs)
        self.fields['username'].widget.attrs.update({
                "placeholder":"username",
            })

        self.fields['email'].widget.attrs.update({
                "placeholder":"email"
            })

class searchForm(forms.Form):
    username = forms.CharField(label='',)
   
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].widget.attrs.update({
                 "placeholder":"search by username"
             })