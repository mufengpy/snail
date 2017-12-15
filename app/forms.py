# coding:utf-8 
__author__ = 'hy'
from snail.form import Forms, Fields


class LoginForm(Forms.Form):
    username = Fields.StringField(error={'required': '用户名不能为空'})
    password = Fields.StringField(error={'required': '密码不能为空'})
    email = Fields.EmailField(error={'required': '邮箱不能为空', 'invalid': '邮箱格式错误'})


