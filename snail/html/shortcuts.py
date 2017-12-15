# coding:utf-8 
__author__ = 'hy'
from jinja2 import Template
from jinja2 import FileSystemLoader, Environment
from snail import reverse
from snail.conf import TEMPLATES_PATH

import re


def HttpResponse(args):
    template = Template('{{ value }}')
    return template.render(value=args).encode('utf-8')


# def rendertest(html, **kwargs):
#     f = open(TEMPLATES_PATH + '\\' + html, 'r', encoding='utf-8')
#     data = f.read()
#     f.close()
#     template = Template(data)
#     data = template.render(**kwargs)
#     return data.encode('utf-8')


# def render(html, **kwargs):
#     env = Environment(loader=FileSystemLoader(TEMPLATES_PATH, ))
#     template = env.get_template(html)
#     data = template.render(url_for=url_for, **kwargs).encode('utf-8')
#     return data


# 1.把<link rel="stylesheet" href="/static/css/login.css" />
# 换成{{ link }}

# 2.    <style>  /static/css/login.css 内容 </style> 替换 {{ link }}


def render(html, **kwargs):
    with open(TEMPLATES_PATH + '\\' + html, 'r', encoding='utf-8') as f:
        data = f.read()

    # 替换CSS
    re_link = re.compile(r'(<link.*href="(.*?)".*/>)')
    links = re_link.findall(data)
    for item in links:
        link, link_href = item[0], item[1][1:]
        style_tag = '<style>css_content</style>'
        # link标签替换为style标签
        link_to_style = data.replace(link, style_tag)

        # 读取link标签里的CSS文件
        with open(link_href, 'r', encoding='utf-8') as f:
            css_data = f.read()
        # CSS内容填充到css_content
        css_content_data = link_to_style.replace('css_content', css_data)
        data = css_content_data

    # 替换JS <script src="/static/js/hello.js"></script>　
    re_script = re.compile(r'(<script.*src="(.*?)".*>.*</script>)')
    scripts = re_script.findall(data)
    for item in scripts:
        script, script_src = item[0], item[1][1:]
        js_tag = '<style>js_content</style>'
        # script标签替换为js标签
        script_to_js = data.replace(script, js_tag)

        # 读取script标签里的js文件
        with open(script_src, 'r', encoding='utf-8') as f:
            css_data = f.read()
        # js内容填充到js_content
        js_content_data = script_to_js.replace('js_content', css_data)
        data = js_content_data

    template = Template(data)

    return template.render(reverse=reverse, **kwargs).encode('utf-8')