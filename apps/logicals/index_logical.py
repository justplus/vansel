#!/usr/bin/env python
# coding=utf-8

__author__ = 'zhaoliang'
__email__ = 'zhaoliang@iflytek.com'
__created__ = '15/12/20'

import MySQLdb
from flask import current_app


def list_requirement():
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
        cur.execute('select distinct(requirement_module) from requirement')
        modules = cur.fetchall()
        for module in modules:
            cur.execute('select distinct(requirement_name) from requirement '
                        'where requirement_module=%s', module[0])
            names = cur.fetchall()
            requirement_names = []
            for name in names:
                cur.execute('select requirement_detail from requirement '
                            'where requirement_module=%s and requirement_name=%s', (module[0], name[0]))
                detail = cur.fetchone()
                requirement_name = {
                    'name': name[0],
                    'detail': detail[0]
                }
                requirement_names.append(requirement_name)
            requirement_module = {
                'module': module[0],
                'names': requirement_names
            }
            result.append(requirement_module)
        return result
    except Exception, ex:
        print ex
        return None
