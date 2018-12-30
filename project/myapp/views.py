from django.http import JsonResponse
from .login import *


def login(request):
    response = {}
    file = './vue2_frontend/static/data.json'
    try:
        user_list = read_from_json(file)
        name = request.GET.get('username')
        password = request.GET.get('pwd')

        result = user_login(user_list, name, password)
        if result == 0:
            response['msg'] = 'success'
            response['error_num'] = 0
        elif result == 1:
            response['msg'] = 'failed'
            response['error_num'] = 1

    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


def regist(request):
    response = {}
    file = './vue2_frontend/static/data.json'
    try:
        user_list = read_from_json(file)
        name = request.GET.get('username')
        password = request.GET.get('pwd')

        result, user_list = user_sign_account(user_list, name, password)
        write_to_json(user_list, file)
        if result == 0:
            response['msg'] = 'success'
            response['error_num'] = 0
        elif result == 1:
            response['msg'] = 'failed'
            response['error_num'] = 1

    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)
