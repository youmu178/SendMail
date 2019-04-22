# -*- coding: UTF-8 -*-
# !/usr/bin/python3

# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from smtplib import SMTP_SSL

# 设置登录及服务器信息
mail_host = 'smtp.qq.com'
mail_user = '@qq.com'
mail_pass = ''
sender = '@qq.com'
receivers = ['@.cn']

# 设置eamil信息
# 添加一个MIMEmultipart类，处理正文及附件
message = MIMEMultipart()
message['From'] = sender
message['To'] = receivers[0]
message['Subject'] = '方案明细'


# 推荐使用html格式的正文内容，这样比较灵活，可以附加图片地址，调整格式等
# with open('abc.html', 'r') as f:
#     content = f.read()
# # 设置html格式参数
# part1 = MIMEText(content, 'html', 'utf-8')
# 添加一个txt文本附件
# with open('abc.txt', 'r')as h:
#     content2 = h.read()
# 设置txt参数
# text = MIMEText(content2, 'plain', 'utf-8')
# 附件设置内容类型，方便起见，设置为二进制流
# text['Content-Type'] = 'application/octet-stream'
# 设置附件头，添加文件名
# text['Content-Disposition'] = 'attachment;filename="abc.txt"'
# 添加照片附件
# with open('1.png', 'rb')as fp:
#     picture = MIMEImage(fp.read())
#     # 与txt文件设置相似
#     picture['Content-Type'] = 'application/octet-stream'
#     picture['Content-Disposition'] = 'attachment;filename="1.png"'
# 将内容附加到邮件主体中
# message.attach(part1)
# message.attach(text)
# message.attach(picture)

def sendPlanMail(plan_text):
    content = ""
    for plan in plan_text:
        content += plan
    text = MIMEText(content, 'plain', 'utf-8')
    message.attach(text)
    sendMail()


def sendMail():
    try:
        smtp = SMTP_SSL(mail_host)
        smtp.set_debuglevel(1)
        smtp.ehlo(mail_host)
        smtp.login(mail_user, mail_pass)
        smtp.sendmail(
            sender, receivers, message.as_string())
        print('success')
        smtp.quit()
    except smtplib.SMTPException as e:
        print('error', e)

