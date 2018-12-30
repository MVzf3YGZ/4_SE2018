from .function2 import *
import myapp.login
from spider_app.spider_top import spider_get
from django.http import JsonResponse
from .func1 import *
from .func3 import *
from .func4 import *
from .func5 import *
import json


def function1(request):
    response = {}
    filename = []
    q_month = []
    temp = {}
    year = request.GET.get('year')
    month = request.GET.get('month')
    quarter = request.GET.get('quarter')

    try:
        if len(month) < 2:
            month = '0' + month
        if quarter == '1':
            q_month = ['01', '02', '03']
        elif quarter == '2':
            q_month = ['04', '05', '06']
        elif quarter == '3':
            q_month = ['07', '08', '09']
        elif quarter == '4':
            q_month = ['10', '11', '12']
        # ¼¾¶È
        for i in range(3):
            flag = spider_get(year + '-' + q_month[i] + 's', 'Month')
            print(flag)
            print(year + '-' + q_month[i] + 's')
            filename.append('./jsonfile/' + year + '-' + q_month[i] + 's.json')
            print(quarter)
            with open(filename[i], 'r', encoding='UTF-8')as f:
                temp = dict(temp, **json.loads(f.read()))
                f.close()

        # print(temp)
        q_result = func1(temp)
        print(q_result)
        myapp.login.write_to_json(q_result, './vue2_frontend/static/' + 'func1-1-' + year + quarter + '.json')

        # ÔÂ·Ý
        spider_get(year + '-' + month + 's', 'Month')
        filename.append('./jsonfile/' + year + '-' + month + 's.json')
        data_m = myapp.login.read_from_json(filename[3])
        m_result = func1(data_m)
        myapp.login.write_to_json(m_result, './vue2_frontend/static/' + 'func1-2-' + year + month + '.json')

        response['msg'] = 'success'
        response['error_num'] = 0

    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


def func2(request):
    response = {}
    file = './jsonfile'
    try:
        year = request.GET.get('year')
        # seq = request.GET.get('seq')
        start_month = request.GET.get('start_month')
        end_month = request.GET.get('end_month')

        box_data = []
        for i in range(int(start_month), int(end_month) + 1):
            if i < 10:
                temp = {}
                file_name = year + '-0' + str(i) + 's'
                flag = spider_get(file_name, 'Month')
                if flag:
                    data = myapp.login.read_from_json(file + '/' + file_name + '.json')
                    box_sum = ticket_box(data)
                    temp['month'] = str(i)
                    temp['box_sum'] = box_sum
                    box_data.append(temp)
            else:
                temp = {}
                file_name = year + '-' + str(i) + 's'
                flag = spider_get(file_name, 'Month')
                print(file_name)
                if flag:
                    data = myapp.login.read_from_json(file + '/' + file_name + '.json')
                    box_sum = ticket_box(data)
                    temp['month'] = str(i)
                    temp['box_sum'] = box_sum
                    box_data.append(temp)

        myapp.login.write_to_json(box_data, './vue2_frontend/static/' + 'func2-' + year + '.json')

        response['msg'] = 'success'
        response['error_num'] = 0

    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


def func2_1(request):
    response = {}
    file = './jsonfile'
    try:
        years = []
        year1 = request.GET.get('year1')
        years.append(year1)
        year2 = request.GET.get('year2')
        years.append(year2)
        year3 = request.GET.get('year3')
        years.append(year3)
        start_month = request.GET.get('start_month')
        end_month = request.GET.get('end_month')

        for year in years:
            box_data = []
            for i in range(int(start_month), int(end_month) + 1):
                if i < 10:
                    temp = {}
                    file_name = year + '-0' + str(i) + 's'
                    spider_get(file_name, 'Month')
                    data = myapp.login.read_from_json(file + '/' + file_name + '.json')
                    box_sum = ticket_box(data)
                    temp['month'] = str(i)
                    temp['box_sum'] = box_sum
                    box_data.append(temp)
                    print(box_data)
                else:
                    temp = {}
                    file_name = year + '-' + str(i) + 's'
                    spider_get(file_name, 'Month')
                    data = myapp.login.read_from_json(file + '/' + file_name + '.json')
                    box_sum = ticket_box(data)
                    temp['month'] = str(i)
                    temp['box_sum'] = box_sum
                    box_data.append(temp)

            myapp.login.write_to_json(box_data, './vue2_frontend/static/' + 'func2-' + year + '.json')

        response['msg'] = 'success'
        response['error_num'] = 0

    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


def function4(request):
    response = {}
    try:
        year = request.GET.get('year')
        num = request.GET.get('num')
        spider_get(year + 's', 'Year')
        filename = './jsonfile/' + year + 's.json'
        temp = myapp.login.read_from_json(filename)
        result = func4(temp, int(num))
        # print(result)
        myapp.login.write_to_json(result, './vue2_frontend/static/' + 'func4-' + year + '.json')

        response['msg'] = 'success'
        response['error_num'] = 0

    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


def function3(request):
    response = {}
    try:
        year = request.GET.get('year')
        num = request.GET.get('num')
        spider_get(year + 's', 'Year')
        filename = ('./jsonfile/' + year + 's.json')
        temp = myapp.login.read_from_json(filename)
        male, female = func3(temp, num)
        # print(male)
        # print(num)
        myapp.login.write_to_json(male, './vue2_frontend/static/' + 'func3-M-' + year + '.json')
        myapp.login.write_to_json(female, './vue2_frontend/static/' + 'func3-F-' + year + '.json')
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


def function_get(request):
    response = {}
    try:
        file_name = request.GET.get('file_name')
        data = myapp.login.read_from_json('./vue2_frontend/static/' + file_name)
        response['index'] = data
        # print(response['index'])

    except Exception as e:
        response['index'] = 1

    return JsonResponse(response)


def function_get2(request):
    response = {}
    try:
        file_name1 = request.GET.get('file_name1')
        file_name2 = request.GET.get('file_name2')
        data1 = myapp.login.read_from_json('./vue2_frontend/static/' + file_name1)
        data2 = myapp.login.read_from_json('./vue2_frontend/static/' + file_name2)
        response['index1'] = data1
        response['index2'] = data2
        # print(response['index'])

    except Exception as e:
        response['index1'] = 1
        response['index2'] = 1

    return JsonResponse(response)


def function_get3(request):
    response = {}
    try:
        file_name1 = request.GET.get('file_name1')
        file_name2 = request.GET.get('file_name2')
        file_name3 = request.GET.get('file_name3')
        data1 = myapp.login.read_from_json('./vue2_frontend/static/' + file_name1)
        data2 = myapp.login.read_from_json('./vue2_frontend/static/' + file_name2)
        data3 = myapp.login.read_from_json('./vue2_frontend/static/' + file_name3)
        response['index1'] = data1
        response['index2'] = data2
        response['index3'] = data3
        # print(response['index'])

    except Exception as e:
        response['index1'] = 1
        response['index2'] = 1
        response['index3'] = 1

    return JsonResponse(response)


def function5(request):
    response = {}
    try:
        strs = request.GET.get('strs')
        filename = request.GET.get('filename')
        func5(strs, filename)
        response['msg'] = 'success'
        response['error_num'] = 0

    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)
