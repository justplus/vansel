#!/usr/bin/env python
# coding=utf-8

__author__ = 'zhaoliang'
__email__ = 'zhaoliang@iflytek.com'
__created__ = '15/12/20'

import MySQLdb
from flask import current_app
import time


def requirement_update_info(project_id):
    database_config = current_app.config['DATABASE_URI']
    conn = MySQLdb.connect(
        host=database_config['host'],
        user=database_config['user'],
        passwd=database_config['passwd'],
        port=database_config['port'],
        db=database_config['db'],
        charset=database_config['charset'])
    cur = conn.cursor()
    cur.execute('select count(*) as total_update_count from project_requirement where project_id=%s', project_id)
    result = cur.fetchone()
    total_update_count = result[0]
    cur.execute('select requirement_url, create_time from project_requirement where project_id=%s order by id desc limit 1', project_id)
    result = cur.fetchone()
    requirement_url = result[0] if result and len(result) > 0 else ''
    create_time = result[1] if result and len(result) > 0 else time.time()
    return total_update_count, requirement_url, create_time

def list_requirement(project_id, project_requirement_id=None):
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
        if project_requirement_id:
            cur.execute('select distinct(requirement_module) from requirement left join project_requirement '
                    'on requirement.project_requirement_id=project_requirement.id '
                    'where project_requirement.id=%s', project_requirement_id)
        else:
            cur.execute('select distinct(requirement_module) from requirement left join project_requirement '
                        'on requirement.project_requirement_id=project_requirement.id '
                        'where project_requirement.project_id=%s and project_requirement.id='
                        '(select max(project_requirement.id) from project_requirement where project_id=%s)', (project_id, project_id))
        modules = cur.fetchall()
        for module in modules:
            if project_requirement_id:
                cur.execute('select distinct(requirement_name) from requirement left join project_requirement '
                        'on requirement.project_requirement_id=project_requirement.id '
                        'where requirement_module=%s and project_requirement.id=%s', (module[0], project_requirement_id))
            else:
                cur.execute('select distinct(requirement_name) from requirement left join project_requirement '
                            'on requirement.project_requirement_id=project_requirement.id '
                            'where requirement_module=%s and project_requirement.project_id=%s and project_requirement.id='
                            '(select max(project_requirement.id) from project_requirement where project_id=%s)', (module[0], project_id, project_id))
            names = cur.fetchall()
            requirement_names = []
            for name in names:
                if project_requirement_id:
                    cur.execute('select requirement_detail from requirement left join project_requirement '
                                'on requirement.project_requirement_id=project_requirement.id '
                                'where requirement_module=%s and requirement_name=%s and project_requirement.id=%s', (module[0], name[0], project_requirement_id))
                else:
                    cur.execute('select requirement_detail from requirement left join project_requirement '
                                'on requirement.project_requirement_id=project_requirement.id '
                                'where requirement_module=%s and requirement_name=%s and project_requirement.id='
                                '(select max(project_requirement.id) from project_requirement where project_id=%s)', (module[0], name[0], project_id))
                detail = cur.fetchall()
                requirement_name = {
                    'name': name[0],
                    'detail': '\n'.join([d[0] for d in detail])
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


def update_requirement(content, project_requirement_id):
    database_config = current_app.config['DATABASE_URI']
    conn = MySQLdb.connect(
        host=database_config['host'],
        user=database_config['user'],
        passwd=database_config['passwd'],
        port=database_config['port'],
        db=database_config['db'],
        charset=database_config['charset'])
    cur = conn.cursor()
    cur.execute('update project_requirement set modification=%s '
                'where id=%s', (content, project_requirement_id))
    conn.commit()
    cur.close()
    conn.close()
    return True


def list_requirement_history(project_id):
    database_config = current_app.config['DATABASE_URI']
    conn = MySQLdb.connect(
        host=database_config['host'],
        user=database_config['user'],
        passwd=database_config['passwd'],
        port=database_config['port'],
        db=database_config['db'],
        charset=database_config['charset'])
    cur = conn.cursor()
    cur.execute('select id, requirement_url, create_time, modification from project_requirement '
                'where project_id=%s order by create_time desc', project_id)
    result = cur.fetchall()
    requirements = []
    index = len(result)
    for requirement in result:
        requirements.append({
            'index': index,
            'project_requirement_id': requirement[0],
            'requirement_url': requirement[1],
            'create_time': time.strftime('%Y-%m-%d %H:%M', time.localtime(requirement[2])),
            'modification': requirement[3]
        })
        index -= 1
    return requirements