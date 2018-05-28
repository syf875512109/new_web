#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Stu(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return 'What {} How {}'.format(self.name, self.age)

    def __str__(self):
        return 'name: {}, age:{}'.format(self.name, self.age)


s = Stu('mike', 20)
repr(s)
print('hi')
