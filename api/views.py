from django.http import JsonResponse
from .models import LinkModel #get my own model aka class describing the table and various functions to operate
from django.db import IntegrityError
from .token import rtoken

from listlinks.views import LoginForm, RegisterForm

from django.contrib.auth import authenticate, login, logout

#API
def list_links(request):
	user = request.user
	count = int(request.GET.get('c',default=5)) #get param ?c=x
	count =  count if 0 <= count <= 25 else 5 #check bounds, return 5 on default
	if user.is_superuser:	
		links = LinkModel.objects.filter()[:count].values('destination','token')  #LIMIT count, then get dict
	else:
		links = LinkModel.objects.filter(owner=user)[:count].values('destination','token')  #LIMIT count, then get dict
	return JsonResponse(list(links),safe=False) #this can leak data like private links with xssi... if you are in 2007

#API
def generate_new(request):
	from django.core.validators import URLValidator
	urlvalid = URLValidator(schemes=['http','https']) #url has to start with this...
	url = request.POST.get('url')
	token = request.POST.get('token') #maybe check for premium account??
	user = request.user
	if not user.is_authenticated:
		return JsonResponse({'error':'WSZC - Weź się zaloguj człowieku'}, status = 500)
	try:
		urlvalid(url)
	except:
		return JsonResponse({'error':'invalid url'}, status = 500)

	#check if token is custom
	if token:
		link = LinkModel(url,token,user.id)
	else:
		link = LinkModel(url,rtoken(),user.id)
	print("saving token:",link.token)

	if LinkModel.objects.filter(token=link.token): #no try except because doesnt work for some reason
		print("token is already taken")
		link = LinkModel(url,rtoken(),user.id)
		if LinkModel.objects.filter(token=link.token): #try random token once more, this will fail anyway when someone 
											#inputs an old existing token way back form rng cycle
			print("random token duplicate")
			return JsonResponse({'error':'token error (very bad)'}, status = 500)

	link.save()
	return JsonResponse({'token':link.token})

def delete_link(request):
	token = request.POST.get('token')
	if not request.user.is_superuser:
		to_remove = LinkModel.objects.get(token=token,owner=request.user)
	else:
		to_remove = LinkModel.objects.get(token=token)
	print(to_remove)
	to_remove.delete()
	return JsonResponse({'removed token':token})

def login_api(request):
	form = LoginForm(request.POST)
	if form.is_valid():
		data = form.cleaned_data
		user = authenticate(username=data['uname'],password=data['password'])
		print(user)
		if user:
			login(request,user)
			return JsonResponse({'error':'OK'})
		else:
			return JsonResponse({'error':'Wrong login or password'})

def register_api(request):
	from django.contrib.auth.models import User
	form = RegisterForm(request.POST)
	if form.is_valid():
		data = form.cleaned_data
		uname,email,passwd =data['uname'],data['email'],data['password']
		try:
			User.objects.create_user(username=uname,email=email,password=passwd).save()
		except Exception as e:
			print(e) # don't leak existing users as response!!
			return JsonResponse({'error':'Something went wrong'}) 


		return JsonResponse({'error':'OK'})

def logout_api(request):
	logout(request)
	return JsonResponse('logout success',safe=False)

