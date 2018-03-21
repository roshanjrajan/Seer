from django.conf.urls import url
from . import views

urlpatterns = [
	# /home/
    url(r'^$', views.home, name='home'),

    # /about/
    url(r'^team/', views.team, name='team'),

     # /login/
    url(r'^login/', views.login, name='login'),
]
