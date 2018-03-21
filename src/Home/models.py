# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# from django.utils.encoding import smart_unicode
from django.db import models

# Create your models here.

class SignUp(models.Model):
	first_name = models.CharField(max_length=120, null=True, blank=True)
	last_name = models.CharField(max_length=120, null=True, blank=True)
	email = models.EmailField()
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated_since = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __str__(self):
		return self.email

