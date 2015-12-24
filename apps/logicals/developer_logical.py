#!/usr/bin/env python
# coding=utf-8

__author__ = 'zhaoliang'
__email__ = 'zhaoliang@iflytek.com'
__created__ = '15/12/21'

import MySQLdb
from flask import current_app
from datetime import *

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
        cur.execute('select * from task where project_id=%s order by start_date asc', project_id)
        tasks = cur.fetchall()
        for task in tasks:
            obj = {
                'task_id': task[0],
                'task_name': task[1],
                'user_name': task[2],
                'plan_days': task[3],
                'finished_date': task[4],
                'project_id': task[5],
                'start_date': task[6]
            }
            result.append(obj)
        return result
    except Exception, ex:
        print ex
        return None

def add_tasks(project_id, task_mds):
    task_mds = u"""
    #2015-12-28 08:30:00
#朗读评测-创建作业 章凯 0.5
#朗读评测-录音转码 梁昭 2
#朗读评测-作业展示 梁昭 2
#朗读评测-作业点评 梁昭 2
#课本点读-电子课本库 章凯 4
#课本点读-电子课本书架 章凯 3
#课本点读-电子课本点读 梁昭 5
#作业-异步上传 章凯 6
#设置-更新手机号 梁昭 1
#消息-表现评价 章凯 4
#档案袋-成长寄语 毛秀如 2
#我的-体验馆 毛秀如
#我的-个人信息 梁昭 2
#班级圈-评论 梁昭 3
    """
    tasks = task_mds.split('\n')
    tasks = [task.strip() for task in tasks if task.strip() != u'']
    try:
        if tasks and len(tasks) > 1:
            project_start_dt = datetime.strptime(tasks[0].strip('#'), '%Y-%m-%d %H:%M:%S')
            task_dt = {}
            all_tasks = []
            for i in range(1, len(tasks)):
                c_task = tasks[i]
                task_info = c_task.strip('#').split(' ')
                if task_info and len(task_info) == 3:
                    task_name = task_info[0]
                    user_name = task_info[1]
                    duration = float(task_info[2])
                    last_start_dt = project_start_dt
                    # {u'张三':[{user_name: u'张三', 'task_name': u'', 'from': '', to: '', next: ''}]}
                    if task_dt and task_dt.get(user_name, None) and len(task_dt.get(user_name)) > 0:
                        last_start_dt = task_dt[user_name][-1].get('next', last_start_dt)
                    to_dt, next_dt = _cal_end_dt(last_start_dt, duration)
                    if not task_dt.get(user_name):
                        task_dt[user_name] = []
                    task_dt.get(user_name).append({'user_name': user_name,
                                                       'task_name': task_name,
                                                       'from': last_start_dt,
                                                       'to': to_dt,
                                                       'next': next_dt})
                    all_tasks.append((task_name, user_name, last_start_dt, to_dt, str(duration)))


            #database_config = current_app.config['DATABASE_URI']
            conn = MySQLdb.connect(
                host='127.0.0.1',
                user='root',
                passwd='root',
                port=3306,
                db='vansel',
                charset='utf8')
            cur = conn.cursor()
            cur.executemany('insert into task(task_name, user_name, start_date, finished_date, plan_days, project_id) '
                        'values (%s, %s, %s, %s, %s, 1)', all_tasks)
            conn.commit()
            cur.close()
            conn.close()
    except Exception, ex:
        print ex

def _cal_end_dt(start_dt, duration):
    # 判断start_dt是上午还是下午， 上午时间段为08:30:00-12:00:00 下午时间段为13:00:00-17:30:00
    if start_dt.hour > 12:
        duration += 0.5

    integer_days = int(duration)-1 if int(duration*2) % 2 == 0 else int(duration)
    # float_days = duration - integer_days
    # half_day = True if float_days > 0.2 else False
    for i in range(integer_days):
        start_dt = start_dt + timedelta(days=1)
        if start_dt.weekday() > 4:
            start_dt = start_dt + timedelta(days=2)
    if int(duration*2) % 2 != 0:
        start_dt = datetime(start_dt.year, start_dt.month, start_dt.day, 12, 0, 0)
        next_dt = datetime(start_dt.year, start_dt.month, start_dt.day, 13, 30, 0)
    else:
        start_dt = datetime(start_dt.year, start_dt.month, start_dt.day, 17, 30, 0)
        next_dt = datetime(start_dt.year, start_dt.month, start_dt.day, 8, 30, 0) + timedelta(days=1)
        if next_dt.weekday() > 4:
            next_dt = start_dt + timedelta(days=2)
    return start_dt, next_dt



if __name__ == '__main__':
    add_tasks(1, '')

