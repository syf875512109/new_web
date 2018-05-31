#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from models import User, Message
from utils import log
import random


message_list = []
session = {}


def director(url):
    headers = {
        'Location': url,
    }
    r = response_with_headers(headers, 302)
    r = r + '\r\n'
    return r.encode('utf-8')


def random_id():
    s = 'gasdgfasdfsad6gf5safd5gfagasd'
    st = ''
    for i in range(10):
        st += s[random.randint(0, len(s) -1)]

    return st


def get_cookie(request):
    log('Cookie', request.cookie)
    username = request.cookie.get('user', '游客')
    if username != '游客':
        username = session[username]
    return username


def response_with_headers(headers, code=200):
    header = 'HTTP/1.1 {} OK\r\n'.format(code)
    header += ''.join(['{}: {}\r\n'.format(k, v) for k, v in headers.items()])
    log('header', header)
    return header


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
    h = {
        'Content-Type': 'text/html',
    }
    username = get_cookie(request)
    if request.method == 'POST':
        form = request.form()
        u = User.new(form)
        if u.validate_login():
            s = random_id()
            session[s] = u.username
            h['Set-Cookie'] = 'user={}'.format(s)
            log('h', h)
            result = '登录成功'
        else:
            result = '用户名或密码错误'
    else:
        result = ''

    header = response_with_headers(h)
    body = template('login.html')
    body = body.replace('{{username}}', username)
    body = body.replace('{{result}}', result)
    r = header + '\r\n' + body

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