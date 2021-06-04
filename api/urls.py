from django.urls import path

from . import views
from .token import rng

#####INIT####
rng.state = 0 #static

with open("lasttoken","r") as f: #load last used token, this can't be taken form db without storing date
	prev = f.read().rstrip()
	if prev:
		rng.state = int(prev)
		print("last used token: ",prev)
	#else 0

###INIT END###


urlpatterns = [
	path('links', views.list_links, name="list_view"), #pass http request to the views.index view function
	path('new', views.generate_new),
	path('login',views.login_api),
	path('logout',views.logout_api, name="logout_api")
]