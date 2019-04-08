from django.shortcuts import render,HttpResponse,redirect
from app01 import models
from app01.forms.user import UserModelForm,UpdateUserModelForm,ResetUserModelForm
from rbac.service.urls import memory_reverse

def user_list(request):
    '''
    用户列表
    :param request:
    :return:
    '''

    user_queryset = models.UserInfo.objects.all()


    return render(request,'user_list.html',{'user_queryset':user_queryset})

def user_add(request):

    if request.method == 'GET':
        form = UserModelForm()
        return render(request, 'rbac/role_change.html', {'form':form})

    form = UserModelForm(data=request.POST)

    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request,'user_list'))
    return render(request, 'rbac/role_change.html', {'form': form})

def user_edit(request,pk):
    #pk就是要修改的用户id
    obj = models.UserInfo.objects.filter(pk=pk).first()
    if not obj:
        return HttpResponse('用户不存在')
    if request.method == 'GET':
        form = UpdateUserModelForm(instance=obj)#这个instance就是可以传入默认值
        return render(request, 'rbac/role_change.html', {'form':form})
    form = UpdateUserModelForm(instance=obj,data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request,'user_list'))
    return render(request, 'rbac/role_change.html', {'form': form})

def user_del(request,pk):
    origin_url = memory_reverse(request,'user_list')
    if request.method == 'GET':
        return render(request,'rbac/delete.html',{'cancel':origin_url})
    models.UserInfo.objects.filter(pk=pk).delete()
    return redirect(origin_url)

def user_reset_pwd(request,pk):
    '''
    重置密码
    :param request:
    :param pk:
    :return:
    '''

    # pk就是要修改的用户id
    obj = models.UserInfo.objects.filter(pk=pk).first()
    if not obj:
        return HttpResponse('用户不存在')
    if request.method == 'GET':
        form = ResetUserModelForm()  # 这个instance就是可以传入默认值
        return render(request, 'rbac/role_change.html', {'form': form})
    form = ResetUserModelForm(instance=obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'user_list'))
    return render(request, 'rbac/role_change.html', {'form': form})


