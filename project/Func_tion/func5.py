#≥¢ ‘base64£¨‘› ±Œ¥ÕÍ…∆
import base64


def func5(code, name):
    imgdata = base64.b64decode(code)
    print(code)
    file = open('./vue2_frontend/static/' + name + '.png', 'wb')
    file.write(imgdata)
    file.close()
