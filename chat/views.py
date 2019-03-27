from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .models import Profile
from django.views import generic
from .forms import ProfileUpdateForm, UserUpdateForm
from . import forms
from django.http import JsonResponse
from chatsDB.forms import SendMessageForm
from chatsDB import views as chatsDBviews
from django.db.models import Q

class ProfileView(generic.DetailView):
	template_name = 'chat/profileView.html'
	context_object_name = "user"
	model = User
	slug_field="username"
	slug_url_kwarg="username"

	def get_context_data(self,*args, **kwargs):
		context = super().get_context_data(*args,**kwargs)
		profile = Profile.objects.filter(user=context['object']).first()
		context["status"] = profile.status
		context["profilePic"] = profile.profile_picture.url
		context["authenticated"] = self.request.user.is_authenticated
		return context

class ProfileSettings(LoginRequiredMixin,generic.View):
	template_name="chat/updateProfile.html"

	def get(self,*args,**kwargs):
		self.user_form = UserUpdateForm(instance = self.request.user)
		self.profile_form = ProfileUpdateForm(instance = self.request.user.profile)
		context = {
			"user_form":self.user_form,
			"profile_form":self.profile_form,
			"profilePic":self.request.user.profile.profile_picture.url
		}
		return render(self.request,self.template_name,context)

	def post(self,*args,**kwargs):
		self.user_form = UserUpdateForm(self.request.POST, instance=self.request.user)
		self.profile_form = ProfileUpdateForm(self.request.POST, self.request.FILES, instance=self.request.user.profile)
		context={
				"user_form":self.user_form,
				"profile_form":self.profile_form,
				"profilePic":self.request.user.profile.profile_picture.url
		}

		if self.user_form.is_valid() and self.profile_form.is_valid():
			self.user_form.save()
			self.profile_form.save()
		else:
			return render(self.request,self.template_name,context)

		return redirect('chat-profile-settings')


class UserHome(LoginRequiredMixin, generic.View):
	template_name = 'chat/userHome.html'

	def get(self,*args,**kwargs):
		search_form = forms.searchForm()
		send_message_form = SendMessageForm()
		contacts_detail = chatsDBviews.getContactsDetail(self.request)
		context={
			"search":search_form,
			"send_message_form":send_message_form,
			"contacts":contacts_detail
		}
		return render(self.request,self.template_name,context)


def SearchUser(request):
	search_query = request.GET.get('username').strip()
	user = request.GET.get('user')
	results = User.objects.filter( Q(username__contains=search_query)& ~Q(username=user) ) 

	results = [{
	 			"username":result.username,
	 			"profile_picture":result.profile.profile_picture.url,
	 			"status":result.profile.status
	 			}
	 			for result in results
	 		] 

	data = {
			"result":results,
		}
	return JsonResponse(data)