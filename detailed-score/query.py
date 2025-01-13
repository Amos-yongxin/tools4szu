# 本科查询平时分和期末分

import json
import os
from time import sleep

import requests

# 请将抓包到的cookie填入此处
cookie = ""


# do not modify the code below
os.environ['NO_PROXY'] = 'ehall.szu.edu.cn'
burp0_url = "https://ehall.szu.edu.cn:443/jwapp/sys/cjcx/modules/cjcx/xscjcx.do"
cookies = {}
burp0_headers = {"Sec-Ch-Ua": "\"Chromium\";v=\"117\", \"Not;A=Brand\";v=\"8\"",
                 "Accept": "application/json, text/javascript, */*; q=0.01",
                 "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                 "X-Requested-With": "XMLHttpRequest", "Sec-Ch-Ua-Mobile": "?0",
                 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.22.2 Safari/530.37",
                 "Sec-Ch-Ua-Platform": "\"Windows\"", "Origin": "https://ehall.szu.edu.cn",
                 "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty",
                 "Referer": "https://ehall.szu.edu.cn/jwapp/sys/cjcx/*default/index.do",
                 "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "zh-CN,zh;q=0.9", "Connection": "close"}

courseData = []


def queryps(score):
    psQuery = {
        "querySetting": "[{\"name\":\"PSCJ\",\"value\":\"" + str(
            score) + "\",\"linkOpt\":\"and\",\"builder\":\"equal\"}]",
        "pageSize": "100", "pageNumber": "1"}
    ret = requests.post(burp0_url, headers=burp0_headers, cookies=cookies, data=psQuery)
    res = json.loads(ret.text)['datas']['xscjcx']['rows']
    for it in res:
        f = True
        for tmp in courseData:
            if it['KCM'] == tmp['KCM']:
                f = False
                tmp['PSCJ'] = score
                tmp['PSCJXS'] = it['PSCJXS']
                tmp['QMCJ'] = tmp.get('QMCJ', 0)
                tmp['QMCJXS'] = tmp.get('QMCJXS', 0)
                break
        if f:
            courseData.append({'KCM': it['KCM'], 'PSCJ': score, 'PSCJXS': it['PSCJXS'], 'QMCJ': 0, 'QMCJXS': 0})


def queryQM(score):
    psQuery = {
        "querySetting": "[{\"name\":\"QMCJ\",\"value\":\"" + str(
            score) + "\",\"linkOpt\":\"and\",\"builder\":\"equal\"}]",
        "pageSize": "100", "pageNumber": "1"}
    ret = requests.post(burp0_url, headers=burp0_headers, cookies=cookies, data=psQuery)
    res = json.loads(ret.text)['datas']['xscjcx']['rows']
    for it in res:
        f = True
        for tmp in courseData:
            if it['KCM'] == tmp['KCM']:
                f = False
                tmp['QMCJ'] = score
                tmp['QMCJXS'] = it['QMCJXS']
                tmp['PSCJ'] = tmp.get('PSCJ', 0)
                tmp['PSCJXS'] = tmp.get('PSCJXS', 0)
                break
        if f:
            courseData.append({'KCM': it['KCM'], 'QMCJ': score, 'QMCJXS': it['QMCJXS'], 'PSCJ': 0, 'PSCJXS': 0})


def makeCookie():
    cookie_list = cookie.split(';')
    for item in cookie_list:
        item = item.strip()
        items = item.split('=')
        cookies[items[0]] = items[1]


if __name__ == '__main__':
    try:
        makeCookie()
    except Exception as e:
        print("Cookie解析失败")
        exit(0)

    for score in range(0, 101):
        queryps(score)
        sleep(0.2)
        queryQM(score)
        sleep(0.2)
        print(f"当前进度{score}%")

    print("=====================================")
    for course in courseData:
        print(
            f"{course['KCM']}: 平时成绩系数{course['PSCJXS']}, 平时成绩{course['PSCJ']}, 期末成绩系数{course['QMCJXS']}, 期末成绩{course['QMCJ']}"
        )
