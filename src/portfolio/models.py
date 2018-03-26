# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from decimal import Decimal
from django.utils import timezone
from django.db import models

class Transaction(models.Model):
    # account = models.ForeignKey(User?????)
    action = models.CharField(max_length=10)
    date = models.DateField('transaction date')
    security = models.CharField(max_length=10, blank=True)
    shares = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    commission = models.DecimalField(decimal_places=2, max_digits=10,
                                     null=True)
    cash_amount = models.DecimalField(decimal_places=2, max_digits=10,
                                      null=True)
    sec_fee = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    split_ratio = models.DecimalField(decimal_places=2, max_digits=5,
                                      null=True)

    def __unicode__(self):
		return self.action + ' ' + str(self.shares) + ' ' + self.security

