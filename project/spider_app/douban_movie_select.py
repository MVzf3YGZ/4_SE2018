import time
import re
from lxml import etree
import requests
import validator
import datetime
import pymysql

db = pymysql.connect(host='127.0.0.1', port=3306,
                     user='root', passwd='qwerty1601', db='ebotdb', charset='utf8')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36 LBBROWSER'}


def movie_select(movieurl):
    # 隧道代理
    appKey = 'UVVGM2laY3ZQeXhKUkI5ZzpiTXNydHFkQ0pjQW5QSFBJ'
    ip_port = 'transfer.mogumiao.com:9001'
    proxy = {"http": "http://" + ip_port, "https": "https://" + ip_port}
    # 代理失效后请修改headers
    headers = {"Proxy-Authorization": 'Basic ' + appKey}
    # try三次
    try:
        html = requests.get(movieurl, headers=headers, proxies=proxy, verify=False, allow_redirects=False).text
    except:
        time.sleep(0.01)
        try:
            html = requests.get(movieurl, headers=headers, proxies=proxy, verify=False, allow_redirects=False).text
        except:
            time.sleep(0.1)
            try:
                html = requests.get(movieurl, headers=headers, proxies=proxy, verify=False, allow_redirects=False).text
            except:
                return []

    response = etree.HTML(html)  # 使用etree解析
    movie = []
    # 依据集数筛选是否为电影
    regx_ismovie = '//text()[preceding-sibling::span[text()="集数:"]][following-sibling::br]'
    ismovie = response.xpath(regx_ismovie)
    if ismovie:
        return []
    # 名字
    regx_name = '//title/text()'
    try:
        name = response.xpath(regx_name)[0][:-5].strip()
    except IndexError:
        return []
    # 分类
    regx_genres = '//span[@property="v:genre"]/text()'
    genres = response.xpath(regx_genres)
    # 不足3个补全
    while len(genres) < 3:
        genres.append('-')
    genres = genres[:3]
    # 导演
    regx_directors = '//a[@rel="v:directedBy"]/text()'
    director = response.xpath(regx_directors)
    if len(director) > 0:
        director = response.xpath(regx_directors)[0]
    else:
        # 缺失
        director = ['-']
    # 演员表
    regx_casts = '//a[@rel="v:starring"]/text()'
    casts = response.xpath(regx_casts)
    while len(casts) < 5:
        casts.append('-')
    casts = casts[:5]
    # 上映日期
    regx_release = '//span[@property="v:initialReleaseDate"]/@content'
    release = response.xpath(regx_release)
    if release:
        # 以大陆上映日期为准
        flag = re.search('中国大陆', release[0])
        if not flag:
            # 如果未在大陆上映，返回
            return []
        # 格式转换，尝试两次
        release_date = validator.str_to_date(validator.match_date(release[0]))
        if not release_date:
            try:
                release_date = validator.str_to_date(validator.match_date(release[1]))
            except:
                return []
        try:
            # 年份
            release_year = datetime.datetime.strptime(release_date, "%Y-%m-%d").year
        except:
            try:
                release_year = datetime.datetime.strptime(release_date, "%Y").year
            except:
                return []

    else:
        return []
    # 分数
    regx_score = '//strong[@property="v:average"]/text()'
    douban_score = response.xpath(regx_score)
    print("电影: " + name)
    if len(douban_score) > 0:
        douban_score = response.xpath(regx_score)[0]
    else:
        douban_score = ['-']
    movie.append(name)
    for i in range(len(genres)):
        movie.append(genres[i])
    movie.append(director)
    for i in range(len(casts)):
        movie.append(casts[i])
    movie.append(release_date)
    movie.append(release_year)
    # movie.append(runtime)
    movie.append(douban_score)
    return movie
