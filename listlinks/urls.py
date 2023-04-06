from django.urls import path, re_path

from . import views

urlpatterns = [
	path('create', views.create_form, name='create'),
	path('list', views.show_links),
	path('login', views.login, name='login'),
	path('register', views.register, name='register'),
	path('', views.show_links),
	#re_path(r'\w{1,7}',views.redir)
	re_path(r'\w{1,20}',views.redir) #custom links have cap at 20
]