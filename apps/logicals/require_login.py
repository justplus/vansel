#!/usr/bin/env python
# coding=utf-8

__author__ = 'zhaoliang'
__email__ = 'zhaoliang@iflytek.com'
__created__ = '15/12/22'

from flask import session, url_for, redirect, abort
from functools import wraps


def require_login():
    def next(func):
        @wraps(func)
        def decorator(*args, **kw):
            if not session.get('user', None):
                return redirect(url_for('index.login'))
            return func(*args, **kw)
        return decorator
    return next


def require_avaliable_role(role_name):
    def next(func):
        @wraps(func)
        def decorator(*args, **kw):
            if session.get('user', None):
                for project in session['user']['projects']:
                    if project[0] == session['project_id']:
                        current_role_name = project[5]
                        break
                if current_role_name == role_name:
                    return func(*args, **kw)
                else:
                    abort(400)
            else:
                return redirect(url_for('index.login'))
        return decorator
    return next