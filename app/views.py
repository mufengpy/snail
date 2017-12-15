# coding:utf-8 
__author__ = 'hy'
import time

from snail import render, HttpResponse, redirect
from snail.db import session, session_wrapper
from snail.utils import ObjsToDicts

from .models import User
# from .forms import LoginForm


def success(request):
    return render('success.html')


def f1(request):
    """
    处理用户请求，并返回相应的内容
    :param request: 用户请求的所有信息
    :return:
    """
    if request.method == 'GET':
        return render('index.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if request.method == 'POST':
            # form = LoginForm(request)

            # 检查用户输入是否合法
            # if form.is_valid():
            #     print('合法，用户输入内容:', form.value_dict)
            # else:
            #     # 如果不合法，则输出错误信息
            #     print('不合法, 错误信息:', form.error_dict)
            if username == 'hy' and password == 'hypassword':
                return HttpResponse('login success')
            return render('index.html', error='user info error')


def f2(request):
    if request.method == 'GET':
        # id = request.GET.get('id','')
        # return render('article.html', id=id)
        return redirect('/userlist')


def f3(request):
    import pymysql

    # 创建连接
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='dbtest')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("select id,username,password from userinfo")
    user_list = cursor.fetchall()
    cursor.close()
    conn.close()

    content_list = []
    for row in user_list:
        tp = "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % (row['id'], row['username'], row['password'])
        content_list.append(tp)
    content = "".join(content_list)
    return render('userlist.html', hy=content)


@session_wrapper
def f4(request):
    user_list = session.query(User).all()
    user_list = ObjsToDicts(user_list)

    dict = {'xxxxx': user_list, 'user': 'ecithy'}
    return render("hostlist.html", **dict)


@session_wrapper
def f5(request):
    new_user = User(username='hy', password='hypd')

    # 添加到session:
    session.add(new_user)
    session.add_all([
        User(username="hy1", password='hy1pd'),
        User(username="hy2", password='hy2pd'),
    ])
