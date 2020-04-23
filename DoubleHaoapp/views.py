import json
import time

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
    request = json.loads(request.body)
    username = request['username']
    password = request['password']
    try:
        student = Student.objects.get(Sid=username)
        if student.Stype == "1":
            result = {"state": "400", "message": "该用户已经注册"}
            result = json.dumps(result, ensure_ascii=False)
            return HttpResponse(result, content_type="application/json,charset=utf-8")
        else:
            result = {"state": "400", "message": "登陆后改密码哦"}
            result = json.dumps(result, ensure_ascii=False)
            return HttpResponse(result, content_type="application/json,charset=utf-8")
    except:
        # 使用爬虫进行校验用户数据
        url = 'http://localhost:6800/schedule.json'
        data = {'project': 'eduScrapy', 'spider': 'Landingcheck', 'username': username, 'password': password}
        requests.post(url=url, data=data)
        # 等待校验用户数据
        time.sleep(10)
        student = Student.objects.get(Sid=username)
        if student.Stype == "3":
            result = {"state": "400", "message": "用户名密码错误，请输入你教务系统正确的账号和密码"}
            result = json.dumps(result, ensure_ascii=False)
            return HttpResponse(result, content_type="application/json,charset=utf-8")
        else:
            # 新用户更新数据
            Spiderlist = ['pi', 'kcb', 'kccj']
            for spider in Spiderlist:
                data = {'project': 'eduScrapy', 'spider': spider, 'username': username, 'password': password}
                requests.post(url=url, data=data)
            token = student.token
            result = {"state": "200", "message": "注册成功", "token": token}
            result = json.dumps(result, ensure_ascii=False)
            return HttpResponse(result, content_type="application/json,charset=utf-8")


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
        token = jwt.decode(request["token"], settings.SECRET_KEY, algorithm='HS256')
        username = token.get("username")
        password = request['newpassword']
        # 验证更改后密码正确性
        url = 'http://localhost:6800/schedule.json'
        data = {'project': 'eduScrapy', 'spider': 'Landingcheck', 'username': username, 'password': password}
        requests.post(url=url, data=data)
        # 等待校验用户数据
        time.sleep(5)
        student = Student.objects.get(Sid=username)
        if student.Stype == "1":
            # 更新用户数据数据
            Spiderlist = ['pi', 'kcb', 'kccj']
            for spider in Spiderlist:
                data = {'project': 'eduScrapy', 'spider': spider, 'username': username, 'password': password}
                requests.post(url=url, data=data)
            token = student.token
            result = {"state": "400", "message": "更新密码成功", "token": token}
            result = json.dumps(result, ensure_ascii=False)
            return HttpResponse(result, content_type="application/json,charset=utf-8")
        if student.Stype == "3":
            token = student.token
            result = {"state": "400", "message": "用户名密码错误，请输入你教务系统正确的账号和密码", "token": token}
            result = json.dumps(result, ensure_ascii=False)
            return HttpResponse(result, content_type="application/json,charset=utf-8")
    except:
        result = {"state": '400', "message": "更新密码失败,请稍侯再试"}
        result = json.dumps(result, ensure_ascii=False)
        return HttpResponse(result, content_type="application/json,charset=utf-8")


# 登陆 返回token
def Scrapy_login(request):
    request = json.loads(request.body)
    try:
        stu = Student.objects.get(Sid=request['username'])
        if stu.Spassword == int(request['password']):
            token = stu.token
            result = {"state": '200', "message": "登陆成功", "token": token}
            result = json.dumps(result, ensure_ascii=False)
            return HttpResponse(result, content_type='application/json,charset=utf-8')
        else:
            result = {"state": '400', "message": "账号密码不匹配"}
            result = json.dumps(result, ensure_ascii=False)
            return HttpResponse(result, content_type="application/json,charset=utf-8")
    except:
        result = {"state": '400', "message": "账号不存在"}
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
        token = jwt.decode(request["token"], settings.SECRET_KEY, algorithm='HS256')
        username = token.get("username")
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
        token = jwt.decode(request["token"],settings.SECRET_KEY, algorithm='HS256')
        username = token.get("username")
        kcb = Kcb.objects.get(Kid_id=username)
        week = None
        if 'week' in request :
            week = request['week']
        result = {"state": '200', "message": get_course(data=kcb.KcbMessage,week=week - 1)}
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
        token = jwt.decode(request["token"], settings.SECRET_KEY, algorithm='HS256')
        username = token.get("username")
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
    request = json.loads(request.body)
    # 判断是否已经登陆
    if "token" not in request:
        result = {"state": '400', "message": "没有相应的操作权限"}
        result = json.dumps(result, ensure_ascii=False)
        return HttpResponse(result, content_type="application/json,charset=utf-8")
    # token中取得usernam
    token = jwt.decode(request["token"], settings.SECRET_KEY, algorithm='HS256')
    username = token.get("username")
    # 验证用户身份，是管理员才有资格更新数据库，防止接口滥用
    if username != 2017006353:
        result = {"state": '400', "message": "没有相应的操作权限"}
        result = json.dumps(result, ensure_ascii=False)
        return HttpResponse(result, content_type="application/json,charset=utf-8")

    # 对数据库中所有用户进行更新
    Stulist = Student.objects.all()
    for stu in Stulist:
        username = stu.Sid
        password = stu.Spassword
        url = 'http://localhost:6800/schedule.json'
        Spiderlist = ['pi', 'kcb', 'kccj']
        for spider in Spiderlist:
            data = {'project': 'eduScrapy', 'spider': spider, 'username': username, 'password': password}
            requests.post(url=url, data=data)
    result = {"state": '200', "message": "update successed"}
    result = json.dumps(result, ensure_ascii=False)
    return HttpResponse(result, content_type="application/json,charset=utf-8")
