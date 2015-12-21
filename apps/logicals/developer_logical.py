#!/usr/bin/env python
# coding=utf-8

__author__ = 'zhaoliang'
__email__ = 'zhaoliang@iflytek.com'
__created__ = '15/12/21'

import MySQLdb
from flask import current_app

def list_tasks(project_id):
    try:
        result = []
        database_config = current_app.config['DATABASE_URI']
        conn = MySQLdb.connect(
            host=database_config['host'],
            user=database_config['user'],
            passwd=database_config['passwd'],
            port=database_config['port'],
            db=database_config['db'],
            charset=database_config['charset'])
        cur = conn.cursor()
        cur.execute('select * from task where project_id=%s', project_id)
        tasks = cur.fetchall()
        for task in tasks:
            obj = {
                'task_id': task[0],
                'task_name': task[1],
                'user_name': task[2],
                'plan_date': task[3],
                'finished_date': task[4],
                'project_id': task[5]
            }
            result.append(obj)
        return result
    except Exception, ex:
        print ex
        return None