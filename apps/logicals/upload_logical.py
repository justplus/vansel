#!/usr/bin/env python
# coding=utf-8

__author__ = 'zhaoliang'
__email__ = 'zhaoliang@iflytek.com'
__created__ = '15/12/24'


import os
from flask import current_app
import simplejson
from apps.logicals.upload_file import uploadfile
import MySQLdb
import time
import xlrd


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
        cur.execute('insert into project_requirement(requirement_url, project_id, create_time) values (%s, %s, %s)',
            (current_app.config['UPLOAD_BASE_URL'] + filename, project_id, time.time()))
        insert_id = cur.lastrowid
        conn.commit()
        cur.close()
        conn.close()

        requirements = readxls(uploaded_file_path)
        insertToDB(requirements, insert_id)
        print u'更新需求列表成功'
        # js回调数据
        result = uploadfile(name=filename, type=mimetype, size=size)
        return {"files": [result.get_file()], "last_id": insert_id}
    else:
        return None


def get_uploaded():
    files = [f for f in os.listdir(current_app.config['UPLOAD_FOLDER'])
             if os.path.isfile(os.path.join(current_app.config['UPLOAD_FOLDER'], f))]
    file_display = []

    for f in files:
        size = os.path.getsize(os.path.join(current_app.config['UPLOAD_FOLDER'], f))
        file_saved = uploadfile(name=f, size=size)
        file_display.append(file_saved.get_file())

    return simplejson.dumps({"files": file_display})


def gen_file_name(filename):
    """
    If file was exist already, rename it and return a new name
    """
    i = 1
    while os.path.exists(os.path.join(current_app.config['UPLOAD_FOLDER'], filename)):
        name, extension = os.path.splitext(filename)
        name = name.rstrip('_'+str(i-1))
        filename = '%s_%s%s' % (name, str(i), extension)
        i = i + 1
    return filename


def readxls(file_path):
    data = xlrd.open_workbook(file_path)
    table = data.sheet_by_index(1)
    nrows = table.nrows

    result = []
    idx = 0

    for i in range(nrows):
        first_val = table.cell(i, 0).value
        try:
            first_val_int = (int)(first_val)
            requirement_module = table.cell(i, 1).value
            requirement_name = table.cell(i, 2).value
            requirement_detail = table.cell(i, 8).value

            if requirement_module.strip() == '':
                last_obj = result[idx - 1]
                requirement_module = last_obj['module']
            if requirement_name.strip() == '':
                last_obj = result[idx - 1]
                requirement_name = last_obj['name']
            requirement = {
                "module": requirement_module,
                "name": requirement_name,
                "detail": requirement_detail
            }
            result.append(requirement)
            idx += 1
        except Exception, ex:
            print ex
    return result


def insertToDB(requirements, project_requirement_id):
    try:
        database_config = current_app.config['DATABASE_URI']
        conn = MySQLdb.connect(
            host=database_config['host'],
            user=database_config['user'],
            passwd=database_config['passwd'],
            port=database_config['port'],
            db=database_config['db'],
            charset=database_config['charset'])
        cur = conn.cursor()
        result = []
        for requirement in requirements:
            result.append((requirement['module'], requirement['name'], requirement['detail'], project_requirement_id))
        cur.executemany('insert into requirement(requirement_module, requirement_name, requirement_detail, '
                        ' project_requirement_id) values (%s, %s, %s, %s)', result)
        conn.commit()
        cur.close()
        conn.close()
    except Exception, ex:
        print ex