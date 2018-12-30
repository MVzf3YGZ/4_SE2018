# 为上层提供接口
import json
from django.http import HttpResponse
import spider_app.mysql2json as mysql2json
import pymysql
import spider_app.ebot as ebot
import re

db = pymysql.connect(host='127.0.0.1', port=3306,
                     user='root', passwd='qwerty1601', db='ebotdb', charset='utf8')


# con = db.cursor()


def table_exits(table_name, type):
    sql = "show tables;"
    con = db.cursor()
    con.execute(sql)
    tables = [con.fetchall()]
    table_list = re.findall('(\'.*?\')', str(tables))
    table_list = [re.sub("'", '', each) for each in table_list]
    if table_name in table_list:
        mysql2json.sql2json(table_name)
        return 1  # 存在返回1
    else:
        dateinfo = table_name[:-1]
        ebot.E_spider(type, dateinfo)
        mysql2json.sql2json(table_name)
        return 0  # 不存在返回0


def spider_get(date_info, type):
    # date_type = request.GET('type', 'Day')
    # date_info = request.GET('date_info', '2018s')
    table_exits(date_info, type)
    return 1
    # return HttpResponse('200')
