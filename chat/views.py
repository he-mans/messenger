from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .models import Profile
from django.views import generic
from .forms import ProfileUpdateForm, UserUpdateForm

class ProfileView(generic.DetailView):
	template_name = 'chat/profileView.html'
	context_object_name = "user"
	model = User
	slug_field="username"
	slug_url_kwarg="username"

	def get_context_data(self,*args, **kwargs):
		context = super(ProfileView,self).get_context_data(*args,**kwargs)
		profile = Profile.objects.filter(user=context['object']).first()
		context["status"] = profile.status
		context["profilePic"] = profile.profile_picture.url
		context["authenticated"] = self.request.user.is_authenticated
		return context

class ProfileSettings(LoginRequiredMixin,generic.View):
	template_name="chat/updateProfile.html"

	def get(self,*args,**kwargs):
		user_form = UserUpdateForm(instance = self.request.user)
		profile_form = ProfileUpdateForm(instance = self.request.user.profile)
		context={
			"user_form":user_form,
			"profile_form":profile_form,
			"profilePic":self.request.user.profile.profile_picture.url
		}
		return render(self.request,self.template_name,context)

	def post(self,*args,**kwargs):
		user_form = UserUpdateForm(self.request.POST, instance=self.request.user)
		profile_form = ProfileUpdateForm(self.request.POST, self.request.FILES, instance=self.request.user.profile)

		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()

		return redirect('chat-profile-settings')


def userHome(request):
	user=request.user.username
	return render(request, 'chat/userHome.html', {"user":user})
