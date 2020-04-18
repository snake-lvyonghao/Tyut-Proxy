import json

import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from DoubleHaoapp.models import Student, PersonalInformation, Kcb, Kccj
from DoubleHaoapp.tool import get_course


def index(request):
    return render(request,'index.html')


def Scrapy_register(request):
    try:
        request = json.loads(request.body)
        username = request['username']
        password = request['password']
        try:
            student = Student.objects.get(Sid=username)
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

# 获取用户个人信息
def Scrapy_PersonnalInformation(request):
    try:
        request = json.loads(request.body)
        username = request['username']
        password = request['password']
        url = 'http://localhost:6800/schedule.json'
        data = {'project': 'eduScrapy', 'spider': 'pi', 'username': username, 'password': password}
        requests.post(url=url, data=data)
        pi = PersonalInformation.objects.get(ClassId__Sid=username)
        print(pi)
        result = {"state": '200', "message": pi.__toString__()}
        result = json.dumps(result, ensure_ascii=False)
        return HttpResponse(result, content_type="application/json,charset=utf-8")
    except:
        result = {"state": "500", "message": "加载中请稍等并刷新，没有学生信息,请先注册"}
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")

# 获取个人课程表
def Scrapy_Kcb(request):
    try:
        request = json.loads(request.body)
        username = request['username']
        password = request['password']
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
    try:
        request = json.loads(request.body)
        username = request['username']
        password = request['password']
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