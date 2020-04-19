import json

import jwt
import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from DoubleHao import settings
from DoubleHaoapp.models import Student, PersonalInformation, Kcb, Kccj
from DoubleHaoapp.tool import get_course


def index(request):
    return render(request, 'index.html')

# 注册
def Scrapy_register(request):
    try:
        request = json.loads(request.body)
        username = request['username']
        password = request['password']
        try:
            student = Student.objects.get(Sid=username)
            result = {"state": "400", "message": "该用户已经注册"}
            result = json.dumps(result, ensure_ascii=False)
            return HttpResponse(result, content_type="application/json,charset=utf-8")
        except:
            # 保存用户信息
            student = Student.createStudent(username, password)
            student.save()
        result = {"state": '200', "message": student.__toString__()}
        result = json.dumps(result, ensure_ascii=False)
        return HttpResponse(result, content_type="application/json,charset=utf-8")
    except:
        result = {"state": "500", "message": "加载中请稍等并刷新，没有学生信息,请检查用户名与密码"}
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")

# 更新账户信息
def Scrapy_update(request):
    request = json.loads(request.body)
    # 判断是否已经登陆
    if "token" not in request:
        result = {"state": '400', "message": "请先登陆"}
        result = json.dumps(result, ensure_ascii=False)
        return HttpResponse(result, content_type="application/json,charset=utf-8")
    try:
        # token中取得usernam
        token = jwt.decode(request["token"],settings.SECRET_KEY,algorithm='HS256')
        username = token.get("username")
        updata_stu = Student.objects.get(Sid=username)
        updata_stu.Spassword = request["newpassword"]
        result = {"state": '200', "message": "更新密码成功"}
        result = json.dumps(result, ensure_ascii=False)
        return HttpResponse(result, content_type="application/json,charset=utf-8")
    except:
        result = {"state": '400', "message": "更新密码失败"}
        result = json.dumps(result, ensure_ascii=False)
        return HttpResponse(result, content_type="application/json,charset=utf-8")


# Session登陆
# def Scrapy_login(Request):
#     request = json.loads(Request.body)
#     if Request.session.get('is_login', False):
#         result = {"state": '200', "message": "已经登陆了"}
#         result = json.dumps(result, ensure_ascii=False)
#         return HttpResponse(result, content_type="application/json,charset=utf-8")
#     m = Student.objects.get(Sid=request['username'])
#     if m.Spassword == int(request['password']):
#         # 设置session
#         Request.session['Sid'] = m.Sid
#         Request.session['Spassword'] = m.Spassword
#         Request.session['is_login'] = True
#         result = {"state": '200', "message": "登陆成功"}
#         result = json.dumps(result, ensure_ascii=False)
#         return HttpResponse(result, content_type='application/json,charset=utf-8')
#     else:
#         result = {"state": '400', "message": "账号密码不匹配"}
#         result = json.dumps(result, ensure_ascii=False)
#         return HttpResponse(result, content_type="application/json,charset=utf-8")

# 登陆返回token
def Scrapy_login(request):
    request = json.loads(request.body)
    stu = Student.objects.get(Sid=request['username'])
    if stu.Spassword == int(request['password']):
        token = stu.token
        result = {"state": '200', "message": "登陆成功","token":token}
        result = json.dumps(result, ensure_ascii=False)
        return HttpResponse(result, content_type='application/json,charset=utf-8')
    else:
        result = {"state": '400', "message": "账号密码不匹配"}
        result = json.dumps(result, ensure_ascii=False)
        return HttpResponse(result, content_type="application/json,charset=utf-8")

# 登出
def Scrapy_logout(request):
    request = json.loads(request.body)
    # 判断是否已经登陆
    if "token" not in request:
        result = {"state": '400', "message": "当前无账户登陆"}
        result = json.dumps(result, ensure_ascii=False)
        return HttpResponse(result, content_type="application/json,charset=utf-8")
    else:
        result = {"state": '200', "message": "已登出"}
        result = json.dumps(result, ensure_ascii=False)
        return HttpResponse(result, content_type="application/json,charset=utf-8")


# 获取用户个人信息
def Scrapy_PersonnalInformation(request):
    request = json.loads(request.body)
    # 判断是否已经登陆
    if "token" not in request:
        result = {"state": '400', "message": "请先登陆"}
        result = json.dumps(result, ensure_ascii=False)
        return HttpResponse(result, content_type="application/json,charset=utf-8")
    try:
        # token中取得usernam
        token = jwt.decode(request["token"],settings.SECRET_KEY,algorithm='HS256')
        username = token.get("username")
        password = Student.objects.get(Sid=username).Spassword
        url = 'http://localhost:6800/schedule.json'
        data = {'project': 'eduScrapy', 'spider': 'pi', 'username': username, 'password': password}
        requests.post(url=url, data=data)
        pi = PersonalInformation.objects.get(ClassId__Sid=username)
        result = {"state": '200', "message": pi.__toString__()}
        result = json.dumps(result, ensure_ascii=False)
        return HttpResponse(result, content_type="application/json,charset=utf-8")
    except:
        result = {"state": "500", "message": "加载中请稍等并刷新，或没有学生信息,请更改密码为教务处密码"}
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")

# 获取个人课程表
def Scrapy_Kcb(request):
    request = json.loads(request.body)
    # 判断是否已经登陆
    if "token" not in request:
        result = {"state": '400', "message": "请先登陆"}
        result = json.dumps(result, ensure_ascii=False)
        return HttpResponse(result, content_type="application/json,charset=utf-8")
    try:
        # token中取得usernam
        token = jwt.decode(request["token"],settings.SECRET_KEY,algorithm='HS256')
        username = token.get("username")
        password = Student.objects.get(Sid=username).Spassword
        url = 'http://localhost:6800/schedule.json'
        data = {'project': 'eduScrapy', 'spider': 'kcb', 'username': username, 'password': password}
        requests.post(url=url, data=data)
        kcb = Kcb.objects.get(Kid__Sid=username)
        result = {"state": '200', "message": get_course(kcb.KcbMessage)}
        result = json.dumps(result, ensure_ascii=False)
        return HttpResponse(result, content_type="application/json,charset=utf-8")
    except:
        result = {"state": "500", "message": "加载中请稍等并刷新，没有学生信息,请先注册"}
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")


# 获取个人成绩概况
def Scrapy_Kccj(request):
    request = json.loads(request.body)
    # 判断是否已经登陆
    if "token" not in request:
        result = {"state": '400', "message": "请先登陆"}
        result = json.dumps(result, ensure_ascii=False)
        return HttpResponse(result, content_type="application/json,charset=utf-8")
    try:
        # token中取得usernam
        token = jwt.decode(request["token"],settings.SECRET_KEY,algorithm='HS256')
        username = token.get("username")
        password = Student.objects.get(Sid=username).Spassword
        url = 'http://localhost:6800/schedule.json'
        data = {'project': 'eduScrapy', 'spider': 'kccj', 'username': username, 'password': password}
        requests.post(url=url, data=data)
        kccj = Kccj.objects.all().filter(Kid__Sid=username)
        kccjlist = []
        for k in kccj:
            kccjlist.append(k.__toString__())
        result = {"state": '200', "message": kccjlist}
        result = json.dumps(result, ensure_ascii=False)
        return HttpResponse(result, content_type="application/json,charset=utf-8")
    except:
        result = {"state": "500", "message": "加载中请稍等并刷新，或没有学生信息,请先注册"}
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")

# 数据库更新
def update_datebase(request):
    # 目前打算采用定时更新，免去服务器压力
    pass