from django.conf.urls import url
from . import views
from .views import *

urlpatterns = [
	# /home/
    # url(r'^$', views.home, name='home'),
    url(r'^$', TransactionListView.as_view()),
    url(r'^txn/$', TransactionListView.as_view()),
    url(r'^(?P<pk>\d+)/$', TransactionDetailView.as_view()),
    url(r'^txn/(?P<pk>\d+)/$', TransactionDetailView.as_view()),
    url(r'^txn/create/$', TransactionCreateView.as_view()),
    url(r'^(?P<pk>\d+)/delete$', TransactionDeleteView.as_view()),
	url(r'^txn/(?P<pk>\d+)/delete$', TransactionDeleteView.as_view()),

	url(r'^BTC/$', views.BTC, name='BTC'),
	url(r'^ETH/$', views.ETH, name='ETH'),
	url(r'^LTC/$', views.LTC, name='LTC'),
]
