from django import forms
from .models import Messages

class SendMessageForm(forms.ModelForm):
	message = forms.CharField(widget=forms.Textarea, label='')

	class Meta:
		fields=['message']
		model=Messages

	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.fields['message'].widget.attrs.update({
				"class" : "hideScrollBar" ,
				"row" : "1" ,
				"placeholder" :"Type your message here"
			})