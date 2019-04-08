from django.shortcuts import render, redirect, HttpResponse
from app01 import models
from app01.forms.host import HostModelForm, UpdateHostModelForm
from rbac.service.urls import memory_reverse

def host_list(request):
    host_queryset = models.Host.objects.all()
    return render(request, 'host_list.html', {'host_queryset': host_queryset})


def host_add(request):
    if request.method == 'GET':
        form = HostModelForm()
        return render(request, 'rbac/role_change.html', {'form': form})

    form = HostModelForm(data=request.POST)

    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'host_list'))
    return render(request, 'rbac/role_change.html', {'form': form})


def host_edit(request, pk):
    # pk就是要修改的主机id
    obj = models.Host.objects.filter(pk=pk).first()
    if not obj:
        return HttpResponse('用户不存在')
    if request.method == 'GET':
        form = UpdateHostModelForm(instance=obj)  # 这个instance就是可以传入默认值
        return render(request, 'rbac/role_change.html', {'form': form})
    form = UpdateHostModelForm(instance=obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'host_list'))
    return render(request, 'rbac/role_change.html', {'form': form})


def host_del(request, pk):
    origin_url = memory_reverse(request, 'host_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': origin_url})
    models.Host.objects.filter(pk=pk).delete()
    return redirect(origin_url)
