#!/usr/bin/env python
# coding=utf-8

__author__ = 'zhaoliang'
__email__ = 'zhaoliang@iflytek.com'
__created__ = '15/12/22'

import MySQLdb
from flask import current_app


def get_user(account, password):
    database_config = current_app.config['DATABASE_URI']
    conn = MySQLdb.connect(
        host=database_config['host'],
        user=database_config['user'],
        passwd=database_config['passwd'],
        port=database_config['port'],
        db=database_config['db'],
        charset=database_config['charset'])
    cur = conn.cursor()
    cur.execute('select user_id, login_name, user_name from user where login_name=%s and password=%s', (account, password))
    result = cur.fetchone()
    if result:
        user = {
            'user_id': result[0],
            'login_name': result[1],
            'user_name': result[2]
        }
        cur.execute('select project.*, role.role_name from project_user '
                    'left join project on project_user.project_id=project.project_id '
                    'left join role on project_user.role_id=role.role_id '
                    'where project_user.user_id=%s', result[0])
        projects = cur.fetchall()
        user['projects'] = []
        for project in projects:
            user['projects'].append(project)
        return {
            'statusCode': 200,
            'result': user
        }
    else:
        return {
            'statusCode': -1000,
            'msg': u'用户名或密码错误'
        }