from django.shortcuts import render,redirect
from app01 import models
from rbac.service.init_permission import init_permission


def login(request):
    if request.method == 'GET':
        return render(request,'login.html')

    user = request.POST.get('username')
    pwd = request.POST.get('password')

    user_object = models.UserInfo.objects.filter(name=user,password=pwd).first()
    if not user_object:
        return render(request,'login.html',{'error':'用户名或者密码错误'})

    #用户权限信息的初始化
    init_permission(user_object,request)

    return redirect('index')


def logout(request):
    request.session.delete()
    return redirect('login')

def index(request):
    return render(request,'index.html')