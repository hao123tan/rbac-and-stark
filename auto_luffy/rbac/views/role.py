from django.shortcuts import render,redirect,HttpResponse
from django.urls import reverse
from rbac import models
from django import forms
from rbac.forms.role import RoleModelForm



def role_list(request):
    role_queryset = models.Role.objects.all()

    return render(request, 'rbac/role_list.html', {'roles': role_queryset})

def role_add(request):

    if request.method == 'GET':
        form = RoleModelForm()
        return render(request, 'rbac/role_change.html', {'form':form})

    form = RoleModelForm(data=request.POST)

    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:role_list'))
    return render(request, 'rbac/role_change.html', {'form': form})

def role_edit(request,pk):
    #pk就是要修改的角色id
    obj = models.Role.objects.filter(pk=pk).first()
    if not obj:
        return HttpResponse('角色不存在')
    if request.method == 'GET':
        form = RoleModelForm(instance=obj)#这个instance就是可以传入默认值
        return render(request, 'rbac/role_change.html', {'form':form})
    form = RoleModelForm(instance=obj,data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:role_list'))
    return render(request, 'rbac/role_change.html', {'form': form})

def role_del(request,pk):
    origin_url = reverse('rbac:role_list')
    if request.method == 'GET':
        return render(request,'rbac/delete.html',{'cancel':origin_url})
    models.Role.objects.filter(pk=pk).delete()
    return redirect(origin_url)