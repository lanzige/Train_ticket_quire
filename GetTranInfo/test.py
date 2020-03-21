#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Author duzy
# @Time      : 2020/3/15 23:22
# @Author    : duzy
# @File      : test.py
# @Software  : PyCharm
import requests
headers  = {'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
            'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language':'zh-CN,zh;q=0.9,en;q=0.8',
            'content-type':'application/x-www-form-urlencoded; charset=UTF-8',
            'origin':'https://trains.ctrip.com',
            'referer':'https://trains.ctrip.com/TrainBooking/Search.aspx?from=beijingxi&to=shanghai&day=2020-05-02&number=&fromCn=%25E5%258C%2597%25E4%25BA%25AC%25E8%25A5%25BF&toCn=%25E4%25B8%258A%25E6%25B5%25B7'}
url = 'https://trains.ctrip.com'

session = requests.Session()
session.get(url,headers=headers)
print(session.cookies)