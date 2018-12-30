import json
import ssl
import time
import requests
import douban_movie_select
import pymysql

tags = [2018]
db = pymysql.connect(host='127.0.0.1', port=3306,
                     user='root', passwd='qwerty1601', db='ebotdb', charset='utf8')
movies = []
movie_urls = []
for tag in tags:
    cursor = db.cursor()
    cursor.close()
    start = 0  # 从第一页开始
    # 不断请求，直到返回结果为空
    while 1:
        # 拼接需要请求的链接，包括标签和开始编号
        url = 'https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=&start=' + str(
            start) + '&year_range=' + str(tag) + ',' + str(tag)
        # 配置代理
        appKey = 'UVVGM2laY3ZQeXhKUkI5ZzpiTXNydHFkQ0pjQW5QSFBJ'
        ip_port = 'transfer.mogumiao.com:9001'
        proxy = {"http": "http://" + ip_port, "https": "https://" + ip_port}
        # 代理失效后请修改headers
        headers = {"Proxy-Authorization": 'Basic ' + appKey}
        try:
            r = requests.get(url, headers=headers, proxies=proxy, verify=False, allow_redirects=False)
        except requests.exceptions.ProxyError:
            time.sleep(0.5)
            r = requests.get(url, headers=headers, proxies=proxy, verify=False, allow_redirects=False)
        except:
            continue
        result = r.text
        try:
            result = json.loads(result)
        except:
            continue
        result = result['data']
        # 返回结果为空，说明已经没有数据了
        # 完成一个标签的处理，退出循环
        if len(result) == 0:
            break
        # 将每一条数据都加入movies
        for item in result:
            movie_urls.append(item)
            if len(item["url"]) > 0:
                dbdata = douban_movie_select.movie_select(item["url"])
                if dbdata:
                    cursor = db.cursor()
                    sql = "INSERT IGNORE INTO douban" + str(
                        2016) + "db" + " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    cursor.execute(sql, tuple(dbdata))
                    db.commit()
                else:
                    print(item['url'])

        # 使用循环记得修改条件
        # 修改start定义爬取的范围
        start += 20
        if start > 9000:
            cursor.close()
            db.close()
            break
