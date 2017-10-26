from django.contrib.auth import login, authenticate
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View

# Create your views here.
from users.forms import LoginForm, RegisterForm
from users.models import UserProfile, EmailVerifyRecord
from utils.email_send import send_register_email


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            print(1111111111111111111111111)
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")

            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, 'login.html', {'msg': '用户未激活'})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误'})
        else:
            return render(request, 'login.html', {'msg': '', 'login_form': login_form})


class RegisterUserView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html",{"register_form":register_form})

    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email","")
            if UserProfile.objects.filter(username=user_name):
                return render(request,"register.html",{"msg":"用户已存在..."})
            pass_word = request.POST.get("password","")
            user = UserProfile()
            user.username =  user_name
            user.password = make_password(pass_word)
            user.email = user_name
            user.is_active = False
            user.save()
            send_register_email(user_name)
            return HttpResponse("请查收邮件,点击链接激活账号....")
        else:
            return render(request, "register.html", {"register_form": register_form})


class ActiveView(View):
    def get(self,request,active_code):
        all_records = EmailVerifyRecord.objects.filter(code = active_code)
        if all_records:
            for record in all_records:
                user_name = record.email
                user = UserProfile.objects.get(username=user_name)
                if user.is_active == False:
                    user.is_active = True
                    user.save()
                    return HttpResponse("用户激活成功....")
                else:
                    return render(request, "register.html", {"msg": "链接已激活过了....."})
        else:
            return render(request, "register.html", {"msg": "链接不存在...."})

