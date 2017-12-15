# coding:utf-8 
__author__ = 'hy'

import re
import os
import shutil
import socket
import gevent
from gevent import socket, monkey
from app.urls import urlpatterns
from snail.exception import CtrlCException
import http.cookies as Cookie
import datetime
import random
from snail.utils import strtobyte

monkey.patch_all()

contenttype_urlencoded = 'application/x-www-form-urlencoded'
contenttype_multipart = 'multipart/form-data'
COMMON_FILE = ['txt', 'html', 'css', 'js', 'word', 'excel', 'ppt', 'png', 'jpg', 'jpeg', 'zip', 'rar', 'gz']


class ResponseHeader(object):
    def __init__(self, location=None):
        expiration = datetime.datetime.now() + datetime.timedelta(seconds=30)
        cookie = Cookie.SimpleCookie()
        cookie["session"] = random.randint(1, 1000000000)
        cookie["session"]["domain"] = "127.0.0.1"
        cookie["session"]["path"] = "/"
        cookie["session"]["expires"] = expiration.strftime("%a, %d-%b-%Y %H:%M:%S PST")
        self.cookie_response = strtobyte(cookie.output()) + b'\r\n\r\n'

        self.status = b'HTTP/1.1 200 OK\r\n'
        self.contenttype = b"Content-Type: text/html; charset=UTF-8\r\n"
        if location:
            # self.redirect = b'HTTP/1.1 301 OK\r\nLocation: http://127.0.0.1:8080/userlist\r\n'
            self.status = b'HTTP/1.1 301 OK\r\n'
            self.location = b'Location: ' + location + b'\r\n'
            self.redirect = self.status + self.location

        self.all = self.status + self.contenttype + self.cookie_response



class Request(object):
    def __init__(self, body=None, boundary=None, contenttype=None, **dict_requestinfo):
        self.url = dict_requestinfo.get('url')
        self.method = dict_requestinfo.get('method')
        self.protocal = dict_requestinfo.get('protocal')
        self.body = body
        self.contenttype = contenttype
        self.boundary = boundary

        # ####################### 处理GET数据 ###########################
        self.GET = {}

        if '?' in self.url:
            self.args = self.url.split('?')[1]

            if '&' in self.url:
                item_list = self.args.split('&')
                for item in item_list:
                    item_name = item.split('=')[0]
                    item_value = item.split('=')[1]
                    self.GET.setdefault(item_name, item_value)
                # print(self.get)
            else:
                self.GET.setdefault(self.args.split('=')[0], self.args.split('=')[1])
                # print(self.get)

        # ####################### 处理POST数据 ###########################
        self.POST = {}
        if self.contenttype == contenttype_urlencoded:
            # POST数据
            item_list = self.body.split('&')
            for item in item_list:
                item_name = item.split('=')[0]
                item_value = item.split('=')[1]
                self.POST.setdefault(item_name, item_value)

        if self.contenttype == contenttype_multipart:
            if not os.path.exists('media'):
                os.makedirs('media')
            item_post = self.body.split(self.boundary)
            for item in item_post:
                if b'filename' in item:

                    re_image = re.compile(b'\r\n.*name="(.*)".*filename="(.*)"\r\n.*\r\n\r\n(.*)', re.S)
                    image_info = re_image.match(item)
                    if image_info:

                        filename, file_data = image_info.group(2, 3)
                        filename = str(filename, encoding='utf-8')

                        if filename not in os.listdir('media'):
                            # 处理图片、文本等普通文件
                            re_filetype = re.compile('.*\\.(.*)')
                            filetype_info = re_filetype.match(filename)
                            filetype = filetype_info.group(1)
                            if filetype:
                                for i in COMMON_FILE:
                                    if filetype == i:
                                        with open(filename, 'wb') as f:
                                            f.write(file_data)
                                        shutil.move(filename, 'media')
                        else:
                            print('file already in media')
                            break

                else:
                    item = str(item, encoding='utf-8')
                    # print(item)
                    re_field = re.compile(r'\r\n.*name="(.*)"\r\n\r\n(.*)\r\n', re.S)
                    field_info = re_field.match(item)
                    if field_info:
                        field_name, field_value = field_info.group(1, 2)
                        self.POST.setdefault(field_name, field_value)


class Server(object):
    def __init__(self, args):
        self.IP_PORT = args

    @CtrlCException
    def run(self):
        sock = socket.socket()
        sock.bind(self.IP_PORT)
        tip = 'Starting development server at http://{0}:{1}/ \n\n' \
              'Quit the server with CTRL-BREAK.'
        print(tip.format(*self.IP_PORT))
        sock.listen(5)

        while True:
            conn, addr = sock.accept()
            # gevent实现异步socket
            gevent.spawn(self.handle_request, conn)

    def handle_request(self, conn):
        try:
            request = conn.recv(65535)

            if not request:
                conn.close()

            method, url, protocal = str(request.split(b'\r\n')[0], encoding='utf-8').split(' ')
            print(request)

            dict_requestinfo = {
                'method': method,
                'url': url,
                'protocal': protocal,
            }

            if method == 'GET':
                headers = Request(body=None, boundary=None, contenttype=None, **dict_requestinfo)

            if method == 'POST':

                if bytes(contenttype_urlencoded, encoding='utf-8') in request:
                    str_request = str(request, encoding='utf-8')
                    request_header, request_body = str_request.split('\r\n\r\n')
                    headers = Request(body=request_body, boundary=None, contenttype=contenttype_urlencoded,
                                      **dict_requestinfo, )

                if bytes(contenttype_multipart, encoding='utf-8') in request:
                    item_byterequest = request.split(b'\r\n')
                    re_boundary = re.compile(b'.*boundary=(.*)')
                    for item in item_byterequest:
                        boundary_info = re_boundary.search(item)
                        if boundary_info:
                            byteboundary = b'--' + boundary_info.group(1)
                    item_boundary = request.split(byteboundary)
                    byterequest_body = byteboundary + byteboundary.join(item_boundary[1:])
                    headers = Request(body=byterequest_body, boundary=byteboundary, contenttype=contenttype_multipart,
                                      **dict_requestinfo, )

            url = url.split('?')[0] if '?' or '&' in url else url
            func_name = None
            for item in urlpatterns:
                if re.match(item[0], url):
                    func_name = item[1]
                    break

            if func_name:
                response = func_name(headers)
                response_header = ResponseHeader().all
                # if func_name.__name__ == 'f2':
                if isinstance(response, dict):
                    location = strtobyte(response.get('Location'))
                    print(location)
                    response_header = ResponseHeader(location=location).redirect
                conn.send(response_header)

            else:
                response = b"<h1>404 not found</h1>"
                conn.send(b"HTTP/1.1 404 OK\r\n\r\n")


            conn.send(response)

        except Exception as ex:
            print(ex)

        finally:
            conn.close()
