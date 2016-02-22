#! /usr/bin/python
# -*- coding: utf-8 -*-
import os

def write_file(dir, filename, content):
    filename=os.path.join(dir, filename)
    try:
        f = open(filename, 'wb')
        f.write(content)
    except IOError, e:
        print('open file error: %s'%filename)
    f.close()

def read_file(dir, filename):
    filename=os.path.join(dir, filename)
    content = ""
    size = os.path.getsize(filename)
    try:
        f = open(filename, 'rb')
        content = f.read()
    except IOError, e:
        print('open file error: %s'%filename)
    f.close()
    return size, content

def check_and_create_dir(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)
