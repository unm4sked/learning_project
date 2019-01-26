""" Defince url's patterns for learning logs"""
from django.conf.urls import url
from . import views

urlpatterns = [
    # Home Page
    url(r'^$', views.index, name='index'),

    # All topics
    url(r'^topics/$', views.topics, name="topics"),

    # Single topic
    url(r'^topics/(?P<topic_id>\d+)/$', views.topic, name='topic'),

    # Add new topic
    url(r'^new_topic/$', views.new_topic, name='new_topic'),

    # Add new entry
    url(r'^new_entry/(?P<topic_id>\d+)/$', views.new_entry, name='new_entry'),

    # Edit entry
    url(r'^edit_entry/(?P<entry_id>\d+)/$', views.edit_entry, name='edit_entry'),
]
