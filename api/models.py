from django.db import models
import django.contrib.auth

# Create your models here.
class LinkModel(models.Model):
	destination = models.URLField()
	token = models.CharField(max_length=7, primary_key=True)  #linkhub.pl/######
	owner = models.ForeignKey(django.contrib.auth.get_user_model(),on_delete=models.CASCADE) #when user is removed, remove all his links
