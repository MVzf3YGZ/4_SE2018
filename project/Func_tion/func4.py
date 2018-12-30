# 能够动态展示不同年份的前3、5、10名的top电影是什么


def func4(data, top_num):
    a = []
    for item in data['RECORDS'][:]:
        BoxOffice = {}
        BoxOffice['name'] = item['MovieName']
        if item['BoxOffice'] != '':
            BoxOffice['value'] = float(item['BoxOffice'])
        else:
            BoxOffice['value'] = float(0)
        a.append(BoxOffice)
    c = sorted(a, key=lambda x: x['value'], reverse=True)
    return c[:top_num]
