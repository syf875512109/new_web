#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json
from utils import log


def save(data, path):
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        # log('save', path, s, data)
        f.write(s)


def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        # log('load', s)
        return json.loads(s)


class Model(object):

    @classmethod
    def db_path(cls):
        classname = cls.__name__
        path = 'db/{}.txt'.format(classname)
        return path

    @classmethod
    def new(cls, form):
        m = cls(form)
        return m

    @classmethod
    def all(cls):
        path = cls.db_path()
        models = load(path)
        ms = [cls.new(m) for m in models]
        return ms

    @classmethod
    def find_by(cls, **kwargs):
        mode = cls.all()
        data = [m for m in mode]
        for k, v in kwargs.items():
            for args in data:
                if getattr(args, k) == v:
                    return args
        return None

    @classmethod
    def find_all(cls, **kwargs):
        mode = cls.all()
        data = [m.__dict__ for m in mode]
        s = []

        for k, v in kwargs.items():
            for args in data:
                if args[k] == v:
                    s.append(cls(args))
        return s

    def save(self):
        models = self.all()
        if len(models) > 0:
            if self.id is not None:
                index = -1
                for i, m in enumerate(models):
                    if self.id == m.id:
                        index = self.id
                        break
                if index > -1:
                    models[index-1] = self
            else:
                self.id = models[-1].id + 1
                models.append(self)
        else:
            self.id = 1
            models.append(self)
        data = [m.__dict__ for m in models]
        path = self.db_path()
        save(data, path)

    def remove(self):
        models = self.all()
        index = -1
        log('self,', self)
        if self.id is not None:
            for i, m in enumerate(models):
                if self.id == m.id:
                    index = i
                    break
            log('index', index)
            if index >= 0:
                del models[index]

        log('models,', models)
        data = [m.__dict__ for m in models]
        path = self.db_path()
        save(data, path)

    def __repr__(self):
        classname = self.__class__.__name__
        properties = ['{}:({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(classname, s)


class User(Model):
    def __init__(self, form):
        if form.get('id', None):
            self.id = form['id']
        else:
            self.id = None
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    def validate_login(self):
        mode = self.all()
        data = [d.__dict__ for d in mode]
        log('data', data, 'self', self.__dict__)
        if self.find_by(username='gua'):
            return True
        else:
            return False

    def validate_register(self):
        return len(self.username) > 2 and len(self.password) > 2


class Message(Model):
    def __init__(self, form):
        self.author = form.get('author', '')
        self.message = form.get('message', '')


class Todo(Model):
    def __init__(self, form):
        self.username = form.get('username', '')
        if form.get('id', None):
            self.id = form['id']
        else:
            self.id = None
