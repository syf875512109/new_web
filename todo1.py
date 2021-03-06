#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from routes import template, director, response_with_headers
from routes import get_cookie
from models import Todo, User
from utils import log


def todo(request):
    uname = get_cookie(request)
    u = User.find_by(username=uname)
    if u is None:
        return director('/login')
    body = template('todo.html')
    todos = []

    log('Todo.all', Todo.all())

    for t in Todo.find_all(user_id = u.id):
        a = '<a href="/todo/edit?id={}">编辑</a>'.format(t.id)
        b = '<a href="/todo/todo_delete?id={}">删除</a>'.format(t.id)
        s = '<h3>{}: {} {} {}</h3>'.format(t.id, t.username, a, b)
        todos.append(s)
    result = ''.join(todos)
    body = body.replace('{{todos}}', result)
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    r = header + '\r\n' + body
    return r.encode('utf-8')


def todo_add(request):
    uname = get_cookie(request)
    t = User.find_by(username=uname)
    if t is None:
        return director('/login')
    if request.method == 'POST' and request.form().get('username'):
        f = request.form()
        u = Todo.new(f)
        u.user_id = t.id
        u.save()
    return director('/todo')


def edit(request):
    uname = get_cookie(request)
    t = User.find_by(username=uname)
    if t is None:
        return director('/login')


    headers = {
        'Content-Type:': 'text/html',
    }
    todo_id = request.query.get('id', -1)
    if int(todo_id) < 0:
        return director('/error')
    log('todo_id', todo_id)
    u = Todo.find_by(id=int(todo_id))
    if u is None:
        return director('/todo')
    elif u.user_id != t.id:
        return director('/todo')

    log('u,', u)
    body = template('edit.html')
    body = body.replace('{{todo_id}}', str(todo_id))
    body = body.replace('{{todo_username}}', u.username)
    header = response_with_headers(headers)

    r = header + '\r\n' + body
    return r.encode('utf-8')


def todo_update(request):
    uname = get_cookie(request)
    t = User.find_by(username=uname)
    if t is None:
        return director('/login')

    if request.method == 'POST' and request.form().get('username', ''):
        todo_id = request.form().get('id', -1)
        if todo_id != -1:
            u = Todo.find_by(id=int(todo_id))
            if u is None or u.user_id != t.id:
                return director('/todo')
            u.username = request.form().get('username')
            u.save()
    return director('/todo')


def todo_delete(request):
    todo_id = int(request.query.get('id', -1))

    t = Todo.find_by(id=todo_id)
    log('t', t)
    if t is not None:
        t.remove()

    return director('/todo')



todo_dict = {
    '/todo': todo,
    '/todo/add': todo_add,
    '/todo/edit': edit,
    '/todo/todo_update': todo_update,
    '/todo/todo_delete': todo_delete,
}
