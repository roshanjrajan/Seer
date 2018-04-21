# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from decimal import Decimal
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):
    account = models.ForeignKey(User, related_name='members', null=True)
    action = models.CharField(max_length=10)
    date = models.DateField('Date')
    currency = models.CharField(max_length=20, null=True)
    number_of_stocks = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    time = models.TimeField('Time')

    def __unicode__(self):
      return self.action + ' ' + str(self.number_of_stocks) + ' ' + self.security

