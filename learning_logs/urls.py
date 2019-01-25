""" Defince url's patterns for learning logs"""
from django.conf.urls import url
from . import views

urlpatterns = [
    #Page
    url(r'^$', views.index, name='index'),
]
