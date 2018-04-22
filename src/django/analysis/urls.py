from django.conf.urls import url
from . import views

# list of cryptocurrencies we support



urlpatterns = [
	# /home/
	url(r'^$', views.home, name='home'),

	# /analysis/
	url(r'^analysis/$', views.analysis, name='analysis')
]

# for c in cryptocurrencies:
# 	urlpatterns.append(url(r'^profile/'+c+'/$', views.))