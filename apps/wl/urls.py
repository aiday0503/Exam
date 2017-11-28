from django.conf.urls import url
from . import views     

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^logout$', views.logout),
    url(r'^wish_travels/create$', views.wish_travels_create),
    url(r'^wish_travels/add$', views.wish_travels_add),
    url(r'^wish_travels/add/(?P<id>\d+)$', views.add_travel),
    url(r'^travels/destination/(?P<id>\d+)$', views.show_travel),

]