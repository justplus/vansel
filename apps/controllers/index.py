#!/usr/bin/env python
# coding=utf-8

__author__ = 'zhaoliang'
__email__ = 'zhaoliang@iflytek.com'
__created__ = '15/12/19'

from flask import Blueprint, render_template
from apps.logicals import index_logical, developer_logical, test_logical

index_bluerint = Blueprint('index', __name__)


@index_bluerint.route('/')
def index():
    return render_template('index.html', locals=locals())

@index_bluerint.route('/requirement')
def requirement():
    requirements = index_logical.list_requirement()
    return render_template('requirement.html', locals=locals())

@index_bluerint.route('/prototype')
def prototype():
    return render_template('prototype.html', locals=locals())

@index_bluerint.route('/developer')
def developer():
    tasks = developer_logical.list_tasks(1)
    return render_template('developer.html', locals=locals())

@index_bluerint.route('/test')
def test():
    builds = test_logical.list_builds(1)
    return render_template('test.html', locals=locals())

@index_bluerint.route('/login')
def login():
    return render_template('login.html', locals=locals())

@index_bluerint.route('/register')
def register():
    return render_template('register.html', locals=locals())

