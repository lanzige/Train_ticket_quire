#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Author duzy
# @Time      : 2020/3/15 22:58
# @Author    : duzy
# @File      : GetTranName.py
# @Software  : PyCharm
import requests,datetime,re,json,ssl
from bs4 import BeautifulSoup

headers  = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
            'Referer':'https://trains.ctrip.com/TrainBooking/Search.aspx?from=beijing&to=shanghai&day=1&number=&fromCn=%25E5%258C%2597%25E4%25BA%25AC&toCn=%25E4%25B8%258A%25E6%25B5%25B7'
            }

IndexUrl = 'https://trains.ctrip.com/TrainBooking/Search.aspx'
namesUrl = 'https://webresource.ctrip.com/ResTrainOnline/R2/TrainBooking/JS/cityUC.min.js?'


def getReleaseNo():
    '''
    得到版本号，携程中很多参数是用版本号来控制的
    :return: 将版本号以str的方式返回
    '''
    response = requests.get(IndexUrl,headers=headers)
    html = response.text
    soup = BeautifulSoup(html,'lxml')
    releaseNo = soup.head.script.string.strip()
    matchObj = re.match(r'.*= \'(.*)\'.*',releaseNo,re.M | re.I)
    releaseNo = matchObj.group(1)
    if releaseNo is None:
        raise ValueError('找不到版本号！')
    return releaseNo


def getCityNames():
    '''
    根据版本号来获取当前的城市名称，也就是站点名称
    :return:城市名称列表，列表的每一项是元组，元组包含了某个城市的名称以及拼音
    '''
    global  namesUrl
    namesUrl = namesUrl+getReleaseNo()+'.js'
    response = requests.get(namesUrl,headers=headers)
    pattern = re.compile(r'{display:"(.*?)",data:"(.*?)"}')
    result = pattern.findall(response.text)
    if result == [] or result is None:
        raise ValueError('没有获取到城市名称数据')
    return result

def getStationNamesByShort(short):
    '''
    携程有一个地址可以根据get传过去的参数即key=...来返回一个json，json里面有这个缩写可能的所有站点名称
    :param short: 拼音缩写
    :return: 可能站点的列表，列表中元素为元组，每个元组由编号，站点中文名称，站点拼音名称组成
    '''
    url = 'https://m.ctrip.com/restapi/soa2/16042/json/searchStationListByKey?key='+short
    response = requests.get(url, headers=headers)
    result = json.loads(response.text)
    index = 0
    stations = []
    for item in result['stationList']:
        stations.append((index,item['stationName'],item['pinYin']))
        index += 1

    if stations == []:
        raise ValueError('没有获取到站点数据！')
    print(stations)

def getTransList(start,end,trandate):
    '''
    根据出发站点和到达站点以及出发时间，得到火车班次
    :param start: 出发站点，元组（index,中文站点名，站点名拼音）
    :param end: 到达站点，元组（index,中文站点名，站点名拼音）
    :param trandate: 出发时间 yyyy-m-d
    :return:所有的车次
    '''
    global s
    year,moth,day = trandate.split('-')
    DepartureDate = datetime.date(int(year),int(moth),int(day))
    DepartureDateReturn = datetime.date(int(year),int(moth),int(day))+datetime.timedelta(days = 2)
    url = 'https://trains.ctrip.com/TrainBooking/Ajax/SearchListHandler.ashx?Action=getSearchList'
    # value = {"IsBus": 'false', "Filter": "0", "Catalog": "", "IsGaoTie": 'false', "IsDongChe": 'false', "CatalogName": "",
    #          "DepartureCity": start[2], "ArrivalCity": end[2], "HubCity": "", "DepartureCityName": start[1],
    #          "ArrivalCityName": end[1], "DepartureDate": DepartureDate, "DepartureDateReturn": DepartureDateReturn,
    #          "ArrivalDate": "", "TrainNumber": ""}

    value={"IsBus":'false',"Filter":"0","Catalog":"","IsGaoTie":'false',"IsDongChe":'false',"CatalogName":"","DepartureCity":"beijing","ArrivalCity":"shanghai","HubCity":"","DepartureCityName":"北京","ArrivalCityName":"上海","DepartureDate":"2020-03-22","DepartureDateReturn":"2020-04-24","ArrivalDate":"","TrainNumber":""}
    data = {'value':json.dumps(value)}
    response = requests.post(url,headers=headers,data=data)
    result_text = response.text
    trainDataDict = json.loads(result_text)
    for item in trainDataDict['TrainItemsList']:
        print(item)

if __name__ == '__main__':
    # getStationNamesByShort('bjx')
    # getStationNamesByShort('shanghai')
    getTransList((0, '北京西', 'beijingxi'),(1, '上海虹桥', 'shanghaihongqiao'),'2020-03-22')