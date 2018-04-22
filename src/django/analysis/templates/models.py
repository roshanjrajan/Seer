from django.db import models
from django.contrib.auth.models import User

class Diagram(model.Model):
	title = models.CharField(max_length=32)		# diagram title
	image = models.ImageField(upload_to=None,	# diagram image
	        height_field=320, width_field=480,
	         max_length=100, **options)