#!/usr/bin/env python
# coding=utf-8

__author__ = 'zhaoliang'
__email__ = 'zhaoliang@iflytek.com'
__created__ = '15/12/19'

import os


CSRF_ENABLED = True
SECRET_KEY = 'guess what you can and try it'

DATABASE_URI = {
    'host': 'localhost',
    'user': 'root',
    'passwd': 'root',
    'port': 3306,
    'db': 'vansel',
    'charset': 'utf8'
}

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
PROTYPE_PATH = os.path.join(ROOT_PATH, 'cache/protype')