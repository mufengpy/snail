# coding:utf-8
__author__ = 'hy'

import sys, os
import os
import inspect


def get_cur_info():
    target_file = inspect.stack()[1][1:3]

    print(target_file)