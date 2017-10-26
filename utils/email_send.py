#!/usr/bin/env python
# coding=utf-8
import random
import string

from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from zmr_form2.settings import EMAIL_FROM


def genera_rand(code_len=10):
    str = ""
    chars = string.digits + string.ascii_letters
    for i in range(code_len):
        tmp = random.randint(0, len(chars) - 1)
        str += chars[tmp]
    return str


def send_register_email(email, send_type="register"):
    if send_type == "register":
        code = genera_rand(16)
    elif send_type=="update":
        code = genera_rand(4)

    record = EmailVerifyRecord()
    record.code = code
    record.email = email
    record.send_type = send_type
    record.save()

    email_title = ""
    email_body = ""

    if send_type == "register":
        email_title = "欢迎注册毛台平台..."
        email_body = "请点击下面的链接激活账号 http://127.0.0.1/active/{0}".format(code)

    send_status = send_mail(email_title,email_body,EMAIL_FROM,[email,])
    if send_status:
        pass



