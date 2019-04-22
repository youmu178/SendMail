# -*- coding: UTF-8 -*-
# !/usr/bin/python3

import requests
import json
import time

import schedule

from send_mail import sendPlanMail

userName = ""
password = ""


def login():
    url = "http://api.yszfans.com/appAPI/api/v1/nsmp/login"
    data = requests.post(url, data={'userName': userName, 'password': password})
    if 200 == data.status_code:
        json_data = data.json()
        # print('---login--- ', json_data)
        info = json_data.get('info')
        if info.get('token'):
            return info.get('token')
    else:
        return ""


def getPlanList(token):
    url = "http://api.yszfans.com/appAPI/api/v1/nsmp/getPlanAll"
    headers = {'x-token': token}
    data = requests.get(url, headers=headers, params={'rid': '', 'expectedType': ''})
    if 200 == data.status_code:
        json_data = data.json()
        # print('---getPlanList--- ', json_data)
        result = json_data.get('result')
        info = []
        if result:
            for item in result:
                text = getPlanItem(token, item.get('plan_id'))
                info.append(text)
        return info


def getPlanItem(token, plan_id):
    url = "http://api.yszfans.com/appAPI/api/v1/nsmp/planbyid"
    headers = {'x-token': token}
    data = requests.post(url, headers=headers, params={'pid': plan_id})

    if 200 == data.status_code:
        json_data = data.json()
        # print('---getPlanItem--- ', json_data)
        result = json_data.get('result')
        if result:
            plan = result.get('plan')
            # "  方案ID:" + plan.get('plan_id')
            text = plan.get('range_name') + "  方案名称:" + plan.get('expert_name') + "  开始时间:" + plan.get(
                'effective_time') + "  结束时间:" + plan.get(
                'deallineTime') + "  方案:" + plan.get('plan_content').replace('<p>', ' ').replace('</p>', ' ').replace(
                '&nbsp;', '').replace('<br/>', ' ').replace('<span style="white-space: pre;">	</span>',
                                                            ' ') + '\n \n'
            return text


def send():
    token = login()
    if token:
        info = getPlanList(token)
        sendPlanMail(info)


def send_mail_by_schedule():
    schedule.every(5).minutes.do(send)  # 每5分钟执行一次
    # schedule.every().hour.do(send)  # 每小时执行一次
    # schedule.every().day.at("23:00").do(send)  # 每天23:00执行一次
    # schedule.every().monday.do(send)  # 每周星期一执行一次
    # schedule.every().wednesday.at("22:15").do(send)  # 每周星期三22:15执行一次

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    send_mail_by_schedule()
