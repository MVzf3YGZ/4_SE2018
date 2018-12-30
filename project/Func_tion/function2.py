import json


# Æ±·¿Êý¾Ý

def ticket_box(data):
    box_sum = 0
    for i in range(len(data['RECORDS'])):
        box_sum += float(data['RECORDS'][i]['BoxOffice'])
    return box_sum
