# coding:utf-8 
__author__ = 'hy'
'''
if it's Often used, like some variable or funcion or class etc ,That's better that import this;
otherwise,That's better way that snail.xxx,cause it's perfect that Let you remember which variable or funcion or class are in the module
'''

from snail.conf import *

from snail.logger import log

from snail.html import render, HttpResponse

from snail.conf import url, url_for, redirect