from django.shortcuts import render, redirect
from api.models import LinkModel
from django import forms

#form for generating new
def create_form(request):
	return render(request, 'create_form.html')

#here you can see your links (and manage them?)
def show_links(request):
	return render(request, 'list.html')

#login
class LoginForm(forms.Form):
	uname = forms.CharField(label="Username", max_length=64)
	password = forms.CharField(label="Password", max_length=64,widget=forms.PasswordInput)

def login(request):
	form = LoginForm()
	return render(request, 'login.html',{'login_form': form})

def redir(request):
	fromurl = request.path[1:]
	dest = LinkModel.objects.get(token=fromurl).destination
	if dest:
		return redirect(dest)
	return redirect('/')