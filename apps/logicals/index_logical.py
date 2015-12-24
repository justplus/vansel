#!/usr/bin/env python
# coding=utf-8

__author__ = 'zhaoliang'
__email__ = 'zhaoliang@iflytek.com'
__created__ = '15/12/20'

import MySQLdb
from flask import current_app


def list_requirement(project_id):
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
        cur.execute('select distinct(requirement_module) from requirement left join project_requirement '
                    'on requirement.project_requirement_id=project_requirement.id '
                    'where project_requirement.project_id=%s and project_requirement.id='
                    '(select max(project_requirement.id) from project_requirement where project_id=%s)', (project_id, project_id))
        modules = cur.fetchall()
        for module in modules:
            cur.execute('select distinct(requirement_name) from requirement left join project_requirement '
                        'on requirement.project_requirement_id=project_requirement.id '
                        'where requirement_module=%s and project_requirement.project_id=%s and project_requirement.id='
                        '(select max(project_requirement.id) from project_requirement where project_id=%s)', (module[0], project_id, project_id))
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
