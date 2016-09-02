#coding=utf-8

from django.conf.urls import include, url
from . import views

urlpatterns = [
	url(r'^$', views.post_list),
	url(r'^(?P<pk>[0-9]+)/$', views.post_detail),
	url(r'^(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
	#发布功能
	url(r'^(?P<pk>[0-9]+)/publish/$', views.post_publish, name='post_publish'),
	#删除功能
	url(r'^(?P<pk>[0-9]+)/remove/$', views.post_remove, name='post_remove'),
	url(r'^new/$', views.post_new, name='post_new'),
	url(r'^drafts/$', views.post_draft_list, name='post_draft_list'),

]