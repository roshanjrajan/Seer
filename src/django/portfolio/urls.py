from django.conf.urls import url
from . import views
from .views import *

urlpatterns = [
	# /home/
    url(r'^$', port_view.as_view(), name='home'),

    url(r'^txn/$', TransactionListView.as_view()),
    url(r'^txn/(?P<pk>\d+)/$', TransactionDetailView.as_view()),
    url(r'^txn/create/$', TransactionCreateView.as_view()),
	url(r'^txn/(?P<pk>\d+)/delete$', TransactionDeleteView.as_view()),
]
