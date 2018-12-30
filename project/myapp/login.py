import json


# 登录模块，未进行加密，可以完善
def user_login(user_list, user_name, user_password):
    for user in user_list:
        if user["name"] == user_name and user['password'] == user_password:
            return 0
    return 1


def user_sign_account(user_list, user_name, user_password):
    user_info = {}

    for info in user_list:
        if info["name"] == user_name:
            return 1, user_list

    user_info["name"] = user_name
    user_info["password"] = user_password
    user_list.append(user_info)
    return 0, user_list


def write_to_json(data, name):
    js_data = json.dumps(data, indent=4)
    file = open(name, "w")
    file.write(js_data)
    file.close()


def read_from_json(name):
    list = []
    try:
        with open(name, "r", encoding="UTF-8") as json_file:
            data_js = json.load(json_file)
    except json.decoder.JSONDecodeError:
        return list
    else:
        return data_js
