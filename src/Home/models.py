from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete

# Create your models here.
class UserProfile(models.Model):
	user = models.OneToOneField(User)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated_since = models.DateTimeField(auto_now_add=False, auto_now=True)

 	def __str__(self): 
 		return '%s' % (self.user)

def create_profile(sender, **kwargs):
 	if kwargs['created']:
 		user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)

def delete_user(sender, instance=None, **kwargs):
    try:
        instance.user
    except User.DoesNotExist:
        pass
    else:
        instance.user.delete()

post_delete.connect(delete_user, sender=UserProfile)