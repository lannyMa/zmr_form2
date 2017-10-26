from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class UserProfile(AbstractUser):
    image = models.ImageField(upload_to="image/%Y/%m",default="image/default.png",verbose_name="头像")
    nick_name = models.CharField(max_length=50,default="",verbose_name="昵称")
    gender = models.CharField(max_length=50,choices=(("femail","女"),("male","男")), default="femail",verbose_name="性别")
    birth = models.DateField(null=True,blank=True,verbose_name="生日")
    address = models.CharField(max_length=100,default="",verbose_name="地址")
    mobile = models.CharField(max_length=13,verbose_name="手机")

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20,verbose_name="验证码类型")
    email = models.EmailField(max_length=30,verbose_name="邮箱")
    send_type = models.CharField(max_length=30,choices=(("register","注册"),("forget","找回密码"),("update","修改邮箱")),default="register",verbose_name="发送类型")
    send_time = models.DateField(default=datetime.now,verbose_name="添加时间")

    class Meta:
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{0}({1})".format(self.code,self.email)

