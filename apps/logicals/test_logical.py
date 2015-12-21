#!/usr/bin/env python
# coding=utf-8

__author__ = 'zhaoliang'
__email__ = 'zhaoliang@iflytek.com'
__created__ = '15/12/21'

import MySQLdb
from flask import current_app


def list_builds(project_id):
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
        cur.execute('select * from test where project_id=%s order by id desc', project_id)
        builds = cur.fetchall()
        quality_cns = [u'差', u'一般', u'良好', u'优秀']
        for build in builds:
            obj = {
                'build_id': build[0],
                'build_num': build[1],
                'build_content': build[2],
                'build_quality': build[3],
                'added_bugs': build[4],
                'serious_bugs': build[5],
                'remaining_bugs': build[6],
                'build_time': build[7],
                'remark': build[8],
                'build_quality_cn': quality_cns[build[3]]
            }

            result.append(obj)
        return result
    except Exception, ex:
        print ex
        return None