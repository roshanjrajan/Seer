from django.conf.urls import url
from . import views
from django.contrib.auth.views import login


urlpatterns = [
	# /home/
    url(r'^$', views.home, name='home'),
    url(r'^home/', views.home, name='home'),

    # /about/
    url(r'^team/', views.team, name='team'),

    # /register/
    url(r'^register/', views.register, name= 'register'),

    # /login/
    url(r'^login/', login, {'template_name': 'home/login.html'}),

    # /logout/
    url(r'^logout/', views.logout, name='logout'),
]
