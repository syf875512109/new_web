#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import socket
import urllib.parse
from utils import log
from routes import route_dict


class Request(object):
    def __init__(self):
        self.method = 'GET'
        self.path = ''
        self.query = {}
        self.body = ''

    def form(self):
        args = self.body.split('&')
        f = {}
        for arg in args:
            k, v = arg.split('=')
            k = urllib.parse.unquote(k)
            v = urllib.parse.unquote(v)
            f[k] = v
        return f


request = Request()


def error(code=404):

    e = {
        404: b'HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


def connection_recv(c):
    response = b''
    while True:
        r = c.recv(1024)
        response += r
        if len(r) < 1024:
            break
    return r.decode('utf-8')


def parsed_path(path):
    f = path.find('?')
    if f == -1:
        return path, {}
    else:
        path, query_string = path.split('?', 1)
        query = {}
        args = query_string.split('&')
        for arg in args:
            k, v = arg.split('=')
            query[k] = v
        return path, query


def response_for_path(path):
    request.path, request.query = parsed_path(path)
    log('({})({}), ({}), ({})'.format(request.method, request.path, request.query, request.body))
    r = {
        # '/static': route_static,
        # '/': route_index,
        # '/login': route_login
        # '/messages': route_message,
    }
    r.update(route_dict)
    response = r.get(request.path, error)
    return response(request)


def run(host='', port=3000):
    log('start at', '{}:{}'.format(host, port))

    with socket.socket() as s:
        s.bind((host, port))

        while True:
            s.listen(5)

            connection, address = s.accept()

            r = connection_recv(connection)
            if len(r.split()) < 2:
                continue
            path = r.split()[1]
            request.method = r.split()[0]
            request.body = r.split('\r\n\r\n')[1]

            response = response_for_path(path)
            connection.sendall(response)
            connection.close()


if __name__ == '__main__':
    d = {
        'host': '',
        'port': 2000,
    }
    run(**d)
