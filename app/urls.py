# coding:utf-8 
__author__ = 'hy'
from snail.conf.urls import url
from .views import f1, f2, f3, f4, f5, success

urlpatterns = [
    url(r'^/$', f1, name='f1_url'),
    url(r'^/article$', f2, name='f2_url'),
    url(r'^/userlist$', f3, name='userlist'),
    url(r'^/hostlist$', f4),
    url(r'^/addtable$', f5),
    url(r'^/success$', success),
]
