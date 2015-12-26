#!/usr/bin/env python
# coding=utf-8

__author__ = 'zhaoliang'
__email__ = 'zhaoliang@iflytek.com'
__created__ = '15/12/19'

from apps import init_app
from apps.helper.markdown2 import markdown


def md2html():
    mdstr = u'## hhhhehhe\r\n### hhahahha\r\n **你好**'
    print markdown(mdstr)


if __name__ == '__main__':
    app = init_app()
    app.run(host='0.0.0.0', port=8080, debug=True)
    # readxls()
    # md2html()
