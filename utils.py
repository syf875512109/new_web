#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import time


def log(*args, **kw):
    format_1 = '%Y:%m:%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format_1, value)
    print(dt, *args, **kw)