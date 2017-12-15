# coding:utf-8 
__author__ = 'hy'


def ObjsToDicts(objs):
    '''把对象列表转换为字典列表'''
    obj_arr = []

    for obj in objs:
        # 把Object对象转换成Dict对象
        dict = {}
        dict.update(obj.__dict__)
        obj_arr.append(dict)

    return obj_arr
