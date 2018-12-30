# 能够动态展示每年/每季度/每月不同题材的票房份额


def func1(data):
    gener = {}
    for item in data['RECORDS'][:]:
        if item['Genre1'] != '-' and item['Genre1'] not in gener:
            gener[item['Genre1']] = float(item['BoxOffice'])
        elif item['Genre1'] != '-' and item['Genre1'] in gener:
            gener[item['Genre1']] += float(item['BoxOffice'])
        if item['Genre2'] != '-' and item['Genre2'] not in gener:
            gener[item['Genre2']] = float(item['BoxOffice'])
        elif item['Genre2'] != '-' and item['Genre2'] in gener:
            gener[item['Genre2']] += float(item['BoxOffice'])
        if item['Genre3'] != '-' and item['Genre3'] not in gener:
            gener[item['Genre3']] = float(item['BoxOffice'])
        elif item['Genre3'] != '-' and item['Genre3'] in gener:
            gener[item['Genre3']] += float(item['BoxOffice'])
    a = []
    for key in gener.keys():
        movie = {}
        movie['name'] = key
        movie['value'] = gener[key]
        a.append(movie)
    return a



