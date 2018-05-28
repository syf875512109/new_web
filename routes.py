#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from models import User, Message
from utils import log
message_list = []


def template(name):
    path = 'templates/' + name
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def route_index(request):
    headers = 'HTTP/1.1 210 very ok\r\nContent-Type: text/html\r\n'
    body = template('index.html')
    r = headers + '\r\n' + body
    return r.encode('utf-8')


def route_login(request):
    headers = 'HTTP/1.1 200 ok\r\nContent-Type: text/html\r\n'
    if request.method == 'POST':
        form = request.form()
        u = User.new(form)
        if u.validate_login():
            result = '登录成功'
        else:
            result = '用户名或密码错误'
    else:
        result = ''

    body = template('login.html')
    body = body.replace('{{result}}', result)
    r = headers + '\r\n' + body

    return r.encode(encoding='utf-8')


def route_register(request):
    headers = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    if request.method == 'POST':
        form = request.form()
        u = User(form)
        if u.validate_register():
            u.save()
            result = '注册成功<br><pre>{}</pre>'.format(User.all())
        else:
            result = '用户名或密码长度必须大于2'
    else:
        result = ''

    body = template('register.html')
    body = body.replace('{{result}}', result)
    r = headers + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_message(request):
    log('本次请求的method', request.method)
    if request.method == 'POST':
        form = request.form()
        msg = Message.new(form)
        message_list.append(msg)

    msgs = '<br>'.join([str(m) for m in message_list])
    headers = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = template('html_basic.html')
    body = body.replace('{{messages}}', msgs)
    r = headers + '\r\n' + body
    return r.encode('utf-8')


def route_static(request):
    filename = request.query.get('file', 'doge.gif')
    path = 'static/' + filename
    with open(path, 'rb') as f:
        headers = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n'
        imag = headers + b'\r\n' + f.read()
        return imag


route_dict = {
    '/static': route_static,
    '/': route_index,
    '/login': route_login,
    '/register': route_register,
    '/messages': route_message,
}