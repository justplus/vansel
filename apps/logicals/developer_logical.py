#!/usr/bin/env python
# coding=utf-8

__author__ = 'zhaoliang'
__email__ = 'zhaoliang@iflytek.com'
__created__ = '15/12/21'

import MySQLdb
from flask import current_app
from datetime import *
from apps.logicals.upload_file import uploadfile
import MySQLdb
import os
import time


def upload(file, project_id):
    if file:
        filename = gen_file_name(file.filename)
        mimetype = file.content_type
        # 保存文件到服务器
        uploaded_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(uploaded_file_path)
        size = os.path.getsize(uploaded_file_path)
        # 保存到数据库
        database_config = current_app.config['DATABASE_URI']
        conn = MySQLdb.connect(
            host=database_config['host'],
            user=database_config['user'],
            passwd=database_config['passwd'],
            port=database_config['port'],
            db=database_config['db'],
            charset=database_config['charset'])
        cur = conn.cursor()
        cur.execute('insert into project_task(project_id, mpp_url, create_time) values (%s, %s, %s)',
                    (project_id, current_app.config['UPLOAD_BASE_URL'] + filename, time.time()))
        insert_id = cur.lastrowid
        conn.commit()
        cur.close()
        conn.close()
        # js回调数据
        result = uploadfile(name=filename, type=mimetype, size=size)
        return {"files": [result.get_file()], "last_id": insert_id}
    else:
        return None


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
        cur.execute('select * from task left join project_task on task.project_task_id=project_task.id '
                    'where task.project_task_id = (select max(project_task.id) from project_task where project_id=%s) '
                    'order by start_date asc', project_id)
        tasks = cur.fetchall()
        for task in tasks:
            obj = {
                'task_id': task[0],
                'task_name': task[1],
                'user_name': task[2],
                'plan_days': task[3],
                'finished_date': task[4],
                'project_task_id': task[5],
                'start_date': task[6]
            }
            result.append(obj)
        return result
    except Exception, ex:
        print ex
        return None


def list_task_history(project_id):
    database_config = current_app.config['DATABASE_URI']
    conn = MySQLdb.connect(
        host=database_config['host'],
        user=database_config['user'],
        passwd=database_config['passwd'],
        port=database_config['port'],
        db=database_config['db'],
        charset=database_config['charset'])
    cur = conn.cursor()
    cur.execute('select id, mpp_url, mpp_thumb_url, create_time, modification from project_task '
                'where project_id=%s order by create_time desc', project_id)
    result = cur.fetchall()
    tasks = []
    index = len(result)
    for task in result:
        tasks.append({
            'index': index,
            'project_task_id': task[0],
            'mpp_url': task[1],
            'mpp_thumb_url': task[2],
            'create_time': time.strftime('%Y-%m-%d %H:%M', time.localtime(task[3])),
            'modification': task[4]
        })
        index -= 1
    return tasks


def add_tasks(project_task_id, task_mds):
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
                    task_dt.get(user_name).append({
                        'user_name': user_name,
                        'task_name': task_name,
                        'from': last_start_dt,
                        'to': to_dt,
                        'next': next_dt})
                    all_tasks.append((task_name, user_name, last_start_dt, to_dt, str(duration), project_task_id))

            database_config = current_app.config['DATABASE_URI']
            conn = MySQLdb.connect(
                host=database_config['host'],
                user=database_config['user'],
                passwd=database_config['passwd'],
                port=database_config['port'],
                db=database_config['db'],
                charset=database_config['charset'])
            cur = conn.cursor()
            cur.executemany(
                'insert into task(task_name, user_name, start_date, finished_date, plan_days, project_task_id) '
                'values (%s, %s, %s, %s, %s, %s)', all_tasks)
            conn.commit()
            cur.close()
            conn.close()
            return True
    except Exception, ex:
        print ex
        return False


def _cal_end_dt(start_dt, duration):
    # 判断start_dt是上午还是下午， 上午时间段为08:30:00-12:00:00 下午时间段为13:00:00-17:30:00
    if start_dt.hour > 12:
        duration += 0.5

    integer_days = int(duration) - 1 if int(duration * 2) % 2 == 0 else int(duration)
    # float_days = duration - integer_days
    # half_day = True if float_days > 0.2 else False
    for i in range(integer_days):
        start_dt = start_dt + timedelta(days=1)
        if start_dt.weekday() > 4:
            start_dt = start_dt + timedelta(days=2)
    if int(duration * 2) % 2 != 0:
        start_dt = datetime(start_dt.year, start_dt.month, start_dt.day, 12, 0, 0)
        next_dt = datetime(start_dt.year, start_dt.month, start_dt.day, 13, 30, 0)
    else:
        start_dt = datetime(start_dt.year, start_dt.month, start_dt.day, 17, 30, 0)
        next_dt = datetime(start_dt.year, start_dt.month, start_dt.day, 8, 30, 0) + timedelta(days=1)
        if next_dt.weekday() > 4:
            next_dt = start_dt + timedelta(days=2)
    return start_dt, next_dt


def gen_file_name(filename):
    """
    If file was exist already, rename it and return a new name
    """
    i = 1
    while os.path.exists(os.path.join(current_app.config['UPLOAD_FOLDER'], filename)):
        name, extension = os.path.splitext(filename)
        name = name.rstrip('_' + str(i - 1))
        filename = '%s_%s%s' % (name, str(i), extension)
        i = i + 1
    return filename


if __name__ == '__main__':
    add_tasks(1, '')

