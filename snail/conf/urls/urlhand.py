# coding:utf-8 
__author__ = 'hy'

import re
# from snail import render


def url(regex, func, name=None):
    return (regex, func, name)


def url_for(name):
    from app.urls import urlpatterns
    for item in urlpatterns:
        if re.match(item[2], name):
            return item[0][1:-1]


def redirect(name):
    default_url = 'http://127.0.0.1:8080'
    location_url = default_url + name
    dict_location = {'Location': location_url}
    return dict_location

