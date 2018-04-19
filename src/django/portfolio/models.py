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

class CryptocurrencyLog(models.Model):
	slug = models.CharField(max_length=20)
	symbol = models.CharField(max_length=20)
	name = models.CharField(max_length=20)
	date = models.CharField(max_length=10)
	ranknow = models.IntegerField()
	openprice = models.DecimalField(decimal_places=2, max_digits=10, null=False)
	highprice models.DecimalField(decimal_places=2, max_digits=10, null=False)
	lowprice models.DecimalField(decimal_places=2, max_digits=10, null=False)
	closeprice models.DecimalField(decimal_places=2, max_digits=10, null=False)
	volume models.DecimalField(decimal_places=2, max_digits=10, null=False)
	market models.DecimalField(decimal_places=2, max_digits=10, null=False)
	close_ratio models.DecimalField(decimal_places=2, max_digits=10, null=False)
	spread models.DecimalField(decimal_places=2, max_digits=10, null=False)