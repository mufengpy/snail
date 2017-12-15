# coding:utf-8 
__author__ = 'hy'
from snail.logger import log


def CtrlCException(func):  # func=tv
    def inner(*args, **kwargs):  # 参数其实传到了这里
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            out = 'KeyboardInterrupt'
            log(out)
            print(out)

    return inner



