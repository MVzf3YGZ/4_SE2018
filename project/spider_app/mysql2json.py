# 封装一层，直接返回json文件
import pymysql
import json
import pprint
import os

d = os.path.dirname(__file__)
# abspath = os.path.abspath(d)
parent_path = os.path.dirname(d)


def sql2json(tableName):
    db = pymysql.connect(host='127.0.0.1', port=3306,
                         user='root', passwd='qwerty1601', db='ebotdb', charset='utf8')
    cursor = db.cursor()
    sqlSelect = "SELECT a.Irank, a.MovieName,a.BoxOffice,a.SumBoxOffice,b.Director,b.Genre1,b.Genre2,b.Genre3,b.CAST1,b.CAST2,b.CAST3,b.CAST4,b.CAST5 FROM `" + \
                tableName + "` AS a, douban2016db as b where a.MovieName=b.MovieName order by a.Irank"
    cursor.execute(sqlSelect)
    data = cursor.fetchall()
    fields = cursor.description
    column_list = []  # 定义字段名的列表
    for i in fields:
        column_list.append(i[0])
    flag = 0
    with open(parent_path + '/jsonfile/' + str(tableName) + '.json', 'w', encoding='utf-8') as f:
        f.write('{\"RECORDS\":\n[')
        for row in data:
            flag += 1
            result = {}
            for i in range(len(column_list)):
                result[column_list[i]] = str(row[i])
            jsonData = json.dumps(result, ensure_ascii=False)
            if flag == len(data):
                f.write(jsonData + '\n]\n}')
            else:
                f.write(jsonData + ',\n')
    f.close()
