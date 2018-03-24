from django.conf.urls import url
from Portfolio.views import port_view

urlpatterns = [
	# /home/
    url(r'^$', port_view.as_view(), name='home'),
]
