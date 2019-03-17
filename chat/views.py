from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def profile(request,username):
	return render(request,'chat/App.html',{"username":username})

@login_required
def userHome(request):
	user=request.user.username
	return render(request, 'chat/userHome.html', {"user":user})
