from django.conf.urls import url
from . import views

urlpatterns = [
	# /home/
    url(r'^$', views.home, name='home'),
    url(r'^home/', views.home, name='home'),

    # /about/
    url(r'^team/', views.team, name='team'),

    # /register/
    url(r'^register/', views.register, name= 'register'),

    # /login/
    url(r'^login/', views.login, name='login'),

    # /logout/
    url(r'^logout/', views.logout, name='logout'),
]
