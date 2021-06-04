from django.http import JsonResponse
from .models import LinkModel #get my own model aka class describing the table and various functions to operate
from django.db import IntegrityError
from .token import rtoken

from listlinks.views import LoginForm

from django.contrib.auth import authenticate, login, logout

#API
def list_links(request):
	user = request.user
	count = int(request.GET.get('c',default=5)) #get param ?c=x
	count =  count if 0 <= count <= 25 else 5 #check bounds, return 5 on default
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
		return JsonResponse({'error':'WSZC'}, status = 500)
	try:
		urlvalid(url)
	except:
		return JsonResponse({'error':'0'}, status = 500)

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
			return JsonResponse({'error':'-1'}, status = 500)

	link.save()
	return JsonResponse({'token':link.token})

def login_api(request):
	form = LoginForm(request.POST)
	if form.is_valid():
		data = form.cleaned_data
		user = authenticate(username=data['uname'],password=data['password'])
		print(user)
		if user:
			login(request,user)
			return JsonResponse({'git':1},safe=False)
		else:
			return JsonResponse({'niegit':0},safe=False)

def logout_api(request):
	logout(request)
	return JsonResponse('logout success',safe=False)