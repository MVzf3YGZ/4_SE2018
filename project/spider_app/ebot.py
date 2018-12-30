import requests
import json
import datetime
import calendar
import pymysql
from time import sleep

db = pymysql.connect(host='127.0.0.1', port=3306,
                     user='root', passwd='qwerty1601', db='ebotdb', charset='utf8')
#取消爬猫眼，改爬ebot数据库

def getBetweenDay(begin_date, end_date):
    date_list = []
    begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y-%m-%d")
        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)
    return date_list


def getMonth(month):
    begin_date = datetime.datetime.strptime(month, "%Y-%m")
    monthRange = calendar.monthrange(begin_date.year, begin_date.month)
    end_date = datetime.datetime.strptime(str(month) + '-' + str(monthRange[1]), "%Y-%m-%d")
    return begin_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")


class EbotSpider:
    def __init__(self, type, **kwargs):
        self.session = requests.Session()
        if type == 'Year' or type == 'year':
            year_list = kwargs['year_list']
            for year in year_list:
                print('{}'.format(str(year)))
                sql_create_year_tb = "CREATE TABLE " + str(year) + "s\n(" + """
                                                 Irank INT,
                                                 MovieName  CHAR(100),
                                                 BoxOffice FLOAT,
                                                 ShowCount FLOAT,
                                                 AudienceCount FLOAT,
                                                 SumBoxOffice FLOAT,
                                                 ServicePrice VARCHAR(100),
                                                 AvgShowPeople FLOAT,
                                                 PRIMARY KEY(MovieName));
                                                 """
                cursor = db.cursor()
                cursor.execute(sql_create_year_tb)
                db.commit()
                cursor.close()
                self.getMovieDayBoxOfficeList(type, year)
                sleep(5)
        elif type == 'Day' or type == 'day':
            self.type = type
            day_dict = kwargs['day_dict']
            begin_date = day_dict['begin_date']
            end_date = day_dict['end_date']
            day_list = getBetweenDay(begin_date, end_date)
            for day in day_list:
                sql_create_day_tb = "CREATE TABLE `" + str(day) + "s`\n(" + """
                                                 Irank INT,
                                                 MovieName  CHAR(100),
                                                 BoxOffice FLOAT,
                                                 ShowCount FLOAT,
                                                 AudienceCount FLOAT,
                                                 SumBoxOffice FLOAT,
                                                 ServicePrice VARCHAR(100),
                                                 AvgShowPeople FLOAT,
                                                 PRIMARY KEY(MovieName));
                                                 """
                cursor = db.cursor()
                cursor.execute(sql_create_day_tb)
                db.commit()
                cursor.close()
                self.getMovieDayBoxOfficeList(type, day)
                sleep(5)
        elif type == 'Month':
            self.type = type
            month_list = kwargs['month_list']
            for month in month_list:
                sql_create_month_tb = "CREATE TABLE `" + str(month) + "s`\n(" + """
                                                 Irank INT,
                                                 MovieName  CHAR(100),
                                                 BoxOffice FLOAT,
                                                 ShowCount FLOAT,
                                                 AudienceCount FLOAT,
                                                 SumBoxOffice FLOAT,
                                                 ServicePrice VARCHAR(100),
                                                 AvgShowPeople FLOAT,
                                                 PRIMARY KEY(MovieName));
                                                 """
                cursor = db.cursor()
                cursor.execute(sql_create_month_tb)
                db.commit()
                cursor.close()
                self.getMovieDayBoxOfficeList(type, month)
                sleep(5)

    def getMovieDayBoxOfficeList(self, type, date_info):
        page = 1
        if type == 'Year':
            url = 'http://ebotapp.entgroup.cn/API/DataBox/Movie/GetMovieYearBoxOfficeList'
        elif type == 'Day':
            url = 'http://ebotapp.entgroup.cn/API/DataBox/Movie/GetMovieDayBoxOfficeList'
        elif type == 'Month':
            url = 'http://ebotapp.entgroup.cn/API/DataBox/Movie/GetMovieMonthBoxOfficeList'

        while (True):
            if type == 'Month':
                sDate, eDate = getMonth(date_info)
                print(sDate)
                print(eDate)
                data = {
                    'PageIndex': page,
                    'PageSize': '1000',
                    'Order': '201',
                    'OrderType': 'DESC',
                    'UserID': '',
                    'DateSort': type,
                    'sDate': str(sDate),
                    'eDate': str(eDate),
                    'Index': '102,201,202,606,225',
                    'Line': '',
                    'City': '',
                    'CityLevel': '',
                    'ServicePrice': 0 if type == 'Year' else 1,
                }
            else:
                data = {
                    'PageIndex': page,
                    'PageSize': '1000',
                    'Order': '201',
                    'OrderType': 'DESC',
                    'UserID': '',
                    'DateSort': type,
                    'Date': date_info,
                    'sDate': date_info,
                    'eDate': date_info,
                    'Index': '102,201,202,205,203,211,221,222,606,225,251,801,604',
                    'Line': '',
                    'City': '',
                    'CityLevel': '',
                    'ServicePrice': 0 if type == 'Year' else 1,
                }
            headers = {
                'Host': 'ebotapp.entgroup.cn',
                'Origin': 'http://ebotapp.entgroup.cn',
                'Referer': 'http://ebotapp.entgroup.cn/DataBox/Film/Movie/Index',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
            }
            req = self.session.post(url=url, data=data, headers=headers)
            json_data = json.loads(req.text)
            if json_data.get('Data').get('Table2'):
                tuple_1 = ()
                data_list = json_data['Data']['Table2']
                if not len(data_list):
                    print('采集完成...')
                    break
                for data in data_list:
                    if type == 'Day':
                        cursor = db.cursor()

                        # 电影名
                        MovieName = data['MovieName']
                        # 排名
                        Irank = data['Irank']
                        # 今日票房
                        BoxOffice = data['BoxOffice']
                        # 累计票房
                        SumBoxOffice = data['SumBoxOffice']
                        # 场次
                        ShowCount = data['ShowCount']
                        # 人次
                        AudienceCount = data['AudienceCount']
                        # 服务费
                        ServicePrice = data['ServicePrice'] if data['ServicePrice'] is not None else '-'
                        # 场均人次
                        AvgShowPeople = data['AvgShowPeople']
                        data1 = []
                        data1.append(Irank)
                        data1.append(MovieName)
                        data1.append(BoxOffice)
                        data1.append(ShowCount)
                        data1.append(AudienceCount)
                        data1.append(SumBoxOffice)
                        data1.append(ServicePrice)
                        data1.append(AvgShowPeople)

                        sql = "INSERT IGNORE INTO `" + str(date_info) + "s`" + " VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                        cursor.execute(sql, tuple(data1))
                        db.commit()
                    elif type == 'Year':
                        cursor = db.cursor()
                        # 电影名
                        MovieName = data['MovieName']
                        # 排名
                        Irank = data['Irank']
                        # 今日票房
                        BoxOffice = data['BoxOffice']
                        # 累计票房
                        SumBoxOffice = data['SumBoxOffice']
                        # 场次
                        ShowCount = data['ShowCount']
                        # 人次
                        AudienceCount = data['AudienceCount']
                        # 服务费
                        ServicePrice = data['ServicePrice'] if data['ServicePrice'] is not None else '-'
                        # 场均人次
                        AvgShowPeople = data['AvgShowPeople']
                        data1 = []
                        data1.append(Irank)
                        data1.append(MovieName)
                        data1.append(BoxOffice)
                        data1.append(ShowCount)
                        data1.append(AudienceCount)
                        data1.append(SumBoxOffice)
                        data1.append(ServicePrice)
                        data1.append(AvgShowPeople)
                        print(date_info)
                        print(data1)
                        sql = "INSERT IGNORE INTO " + str(date_info) + "s" + " VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                        cursor.execute(sql, tuple(data1))
                        db.commit()
                    elif type == 'Month':
                        print(data)
                        cursor = db.cursor()
                        # 电影名
                        MovieName = data['MovieName']
                        # 排名
                        Irank = data['Irank']
                        # 今日票房
                        BoxOffice = data['BoxOffice']
                        # 累计票房
                        SumBoxOffice = data['BoxOffice']
                        # 场次
                        ShowCount = data['ShowCount']
                        # 人次
                        AudienceCount = data['AudienceCount']
                        # 服务费
                        ServicePrice = '-'
                        # 场均人次
                        AvgShowPeople = '-'
                        data1 = []
                        data1.append(Irank)
                        data1.append(MovieName)
                        data1.append(BoxOffice)
                        data1.append(ShowCount)
                        data1.append(AudienceCount)
                        data1.append(SumBoxOffice)
                        data1.append(ServicePrice)
                        data1.append(AvgShowPeople)
                        print(date_info)
                        print(data1)
                        sql = "INSERT IGNORE INTO `" + str(date_info) + "s`" + " VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                        cursor.execute(sql, tuple(data1))
                        db.commit()
            else:
                break
            page += 1
            sleep(2)


def E_spider(type, dateinfo):
    if type == 'Day':
        day_dict = {
            'begin_date': dateinfo,
            'end_date': dateinfo
        }
        ebotspider = EbotSpider(type, day_dict=day_dict)
    elif type == 'Month':
        month_list = [dateinfo]
        EbotSpider(type, month_list=month_list)
    elif type == 'Year':
        year_list = [dateinfo]
        EbotSpider(type, year_list=year_list)

