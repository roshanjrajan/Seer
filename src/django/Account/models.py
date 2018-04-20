from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

# Create your models here.
class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	profit = models.FloatField(default=0)
	spent = models.FloatField(default=0)
	email_confirmed = models.BooleanField(default=False)
	
	def __str__(self): 
 		return self.user.username

def create_profile(sender, **kwargs):
 	if kwargs['created']:
 		user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)

# @receiver(post_save, sender=User)
# def update_user_profile(sender, instance, created, **kwargs):
# 	if created:
# 		UserProfile.objects.create(user=instance)
		
# 	instance.profile.save()
