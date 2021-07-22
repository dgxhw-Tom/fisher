#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
    @Created on 2021/7/21 下午4:34
    @Author xuhuawei
    @attention： 
'''
from threading import Thread

from flask import render_template, current_app
from flask_mail import Message

from app import mail


def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
            print("邮件发送成功")
        except Exception as e:
            print(e)
            print("邮件发送失败")

'''
如果直接使用 current_app ，LocalStack存储的AppContext，是线程隔离的，所以其他线程访问时是找不到 LocalStack 栈顶 的 AppContext 的，所以会报错 "working outside of application context"

所以需要使用 current_app._get_current_object() 获取一个 AppContext 传入 多线程的function中，才可以有application的上下文信息
'''
def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(
        '[鱼书]' + ' ' + subject,
        sender=app.config['MAIL_DEFAULT_SENDER'],
        recipients=[to]
    )
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
