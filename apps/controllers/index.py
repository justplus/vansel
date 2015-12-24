#!/usr/bin/env python
# coding=utf-8

__author__ = 'zhaoliang'
__email__ = 'zhaoliang@iflytek.com'
__created__ = '15/12/19'

from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from apps.logicals import index_logical, developer_logical, test_logical, login_logical
from apps.logicals.require_login import require_login, require_avaliable_role

index_bluerint = Blueprint('index', __name__)


@index_bluerint.route('/<int:project_id>')
@require_login()
def index(project_id):
    session['project_id'] = project_id
    return render_template('index.html', locals=locals())

@index_bluerint.route('/')
@require_login()
def pindex():
    return render_template('index.html', locals=locals())

@index_bluerint.route('/<int:project_id>/requirement')
@require_login()
def requirement(project_id):
    session['project_id'] = project_id
    requirements = index_logical.list_requirement(project_id)
    return render_template('requirement.html', locals=locals())

@index_bluerint.route('/<int:project_id>/prototype')
@require_login()
def prototype(project_id):
    return render_template('prototype.html', locals=locals())

@index_bluerint.route('/<int:project_id>/developer')
@require_login()
def developer(project_id):
    session['project_id'] = project_id
    tasks = developer_logical.list_tasks(project_id)
    return render_template('developer.html', locals=locals())

@index_bluerint.route('/<int:project_id>/test')
@require_login()
def test(project_id):
    session['project_id'] = project_id
    builds = test_logical.list_builds(project_id)
    return render_template('test.html', locals=locals())

@index_bluerint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if session.get('user', None):
            return redirect(url_for('index.index'))
        return render_template('login.html', locals=locals())
    elif request.method == 'POST':
        account = request.form['account']
        password = request.form['password']
        result = login_logical.get_user(account, password)
        response = jsonify(result)
        if result['statusCode'] == 200:
            #response.set_cookie('user', result['result'], max_age=30*24*60*60)
            session['user'] = result['result']
            session['project_id'] = result['result']['projects'][0][0]
        return response


@index_bluerint.route('/register')
def register():
    return render_template('register.html', locals=locals())


@index_bluerint.route('/logout')
@require_login()
def logout():
    session['user'] = None
    session['project_id'] = None
    return redirect(url_for('index.login'))


@index_bluerint.route('/<int:project_id>/admin/pm')
@require_avaliable_role('product manager')
def pm_admin(project_id):
    return render_template('requirement_admin.html', locals=locals())

