#!/usr/bin/env python
# coding=utf-8

__author__ = 'zhaoliang'
__email__ = 'zhaoliang@iflytek.com'
__created__ = '15/12/19'

from apps import init_app
import xlrd
import os
import MySQLdb
from apps.helper.markdown2 import markdown

# test
def readxls():
    data = xlrd.open_workbook(os.path.join(os.path.expanduser("~"), 'Desktop/1.xlsx'))
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
    insertToDB(result)


def insertToDB(requirements):
    try:
        conn = MySQLdb.connect(host='localhost', user='root', passwd='root', port=3306, db='vansel', charset='utf8')
        cur = conn.cursor()
        result = []
        for requirement in requirements:
            result.append((requirement['module'], requirement['name'], requirement['detail'], 1))
            print (requirement['module'], requirement['name'], '123', 1)
        cur.executemany('insert into requirement(requirement_module, requirement_name, requirement_detail, '
                        ' project_requirement_id) values (%s, %s, %s, %s)', result)
        conn.commit()
        cur.close()
        conn.close()
    except Exception, ex:
        print ex

def md2html():
    mdstr = u'## hhhhehhe\r\n### hhahahha\r\n **你好**'
    print markdown(mdstr)


if __name__ == '__main__':
    app = init_app()
    app.run(host='0.0.0.0', port=8080, debug=True)
    # readxls()
    # md2html()
