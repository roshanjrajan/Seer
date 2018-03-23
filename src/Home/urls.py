from django.conf.urls import url
from . import views
from django.contrib.auth.views import login, logout


urlpatterns = [
	# /home/
    url(r'^$', views.home, name='home'),
    url(r'^home/', views.home, name='home'),

    # /about/
    url(r'^team/', views.team, name='team'),

    # /register/
    url(r'^register/', views.register, name= 'register'),

    # /profile/->edit/
    url(r'^profile/', views.view_profile, name= 'view_profile'),
    url(r'^/profile/edit/', views.edit_profile, name= 'edit_profile'),
    url(r'^delete/(?P<person_pk>.*)$', views.delete_profile),
    
    # /login/ || /logout/
    url(r'^login/', login, {'template_name': 'home/login.html'}),
    url(r'^logout/', logout, {'template_name': 'home/home.html'}),
]
