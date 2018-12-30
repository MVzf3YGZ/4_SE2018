# 能够找出某一年出演电影次数TOP的劳模男女演员
import json


def func3(data, top_num):
    with open(r'Func_tion/name_sex.json', 'r', encoding='utf-8') as f:
        info = json.loads(f.read())['RECORDS'][:]
    cast = {}
    cast_male = []
    cast_female = []
    top_num = int(top_num)
    for item in data['RECORDS'][:]:
        if item['CAST1'] != '-' and item['CAST1'] not in cast:
            cast[item['CAST1']] = 1
        elif item['CAST1'] != '-' and item['CAST1'] in cast:
            cast[item['CAST1']] += 1
        if item['CAST2'] != '-' and item['CAST2'] not in cast:
            cast[item['CAST2']] = 1
        elif item['CAST2'] != '-' and item['CAST2'] in cast:
            cast[item['CAST2']] += 1
        if item['CAST3'] != '-' and item['CAST3'] not in cast:
            cast[item['CAST3']] = 1
        elif item['CAST3'] != '-' and item['CAST3'] in cast:
            cast[item['CAST3']] += 1
        if item['CAST4'] != '-' and item['CAST4'] not in cast:
            cast[item['CAST4']] = 1
        elif item['CAST4'] != '-' and item['CAST4'] in cast:
            cast[item['CAST4']] += 1
        if item['CAST5'] != '-' and item['CAST5'] not in cast:
            cast[item['CAST5']] = 1
        elif item['CAST5'] != '-' and item['CAST5'] in cast:
            cast[item['CAST5']] += 1

    cast_mix = sorted(cast.items(), key=lambda x: x[1], reverse=True)

    for cast_item in cast_mix:
        for sex_item in info:
            if cast_item[0] == sex_item['name']:
                if sex_item['sex'] == '男':
                    cast_male.append(cast_item)
                elif sex_item['sex'] == '女':
                    cast_female.append(cast_item)
            if len(cast_male) > top_num and len(cast_female) > top_num:
                f = []
                m = []
                for i in range(top_num):
                    female = {}
                    male = {}
                    female['name'] = cast_female[i][0]
                    female['value'] = cast_female[i][1]
                    male['name'] = cast_male[i][0]
                    male['value'] = cast_male[i][1]
                    f.append(female)
                    m.append(male)
                return m, f

