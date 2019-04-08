from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from rbac import models
from rbac.forms.menu import MenuModelForm, SecondMenuModelForm, PermissionModelForm, MultiAddPermissionForm, \
    MultiEditPermissionForm
from rbac.service.urls import memory_reverse
from rbac.service.routes import get_all_url_dict
from collections import OrderedDict
from django.forms import formset_factory
from django.conf import settings
from django.utils.module_loading import import_string

def menu_list(request):
    '''
    菜单和权限列表
    :param request:
    :return:
    '''
    menu_id = request.GET.get('mid')  # 用户选择的一级菜单
    menus = models.Menu.objects.all()
    second_menu_id = request.GET.get('sid')  # 用户选择的二级菜单

    menu_exist = models.Menu.objects.filter(id=menu_id).exists()
    if not menu_exist:
        menu_id = None
    if menu_id:
        second_menus = models.Permission.objects.filter(menu_id=menu_id)
    else:
        second_menus = []
    second_menu_exist = models.Permission.objects.filter(id=second_menu_id).first()
    if not second_menu_exist:
        second_menu_id = None
    if second_menu_id:
        permissions = models.Permission.objects.filter(pid_id=second_menu_id)
    else:
        permissions = []

    return render(request, 'rbac/menu_list.html', {
        'menus': menus,
        'menu_id': menu_id,
        'second_menus': second_menus,
        'second_menu_id': second_menu_id,
        'permissions': permissions})


def menu_add(request):
    if request.method == 'GET':
        form = MenuModelForm()
        return render(request, 'rbac/role_change.html', {'form': form})

    form = MenuModelForm(data=request.POST)

    if form.is_valid():
        form.save()
        url = memory_reverse(request, 'rbac:menu_list')
        return redirect(url)
    return render(request, 'rbac/role_change.html', {'form': form})


def menu_edit(request, pk):
    # pk就是要修改的用户id
    obj = models.Menu.objects.filter(pk=pk).first()
    if not obj:
        return HttpResponse('菜单不存在')
    if request.method == 'GET':
        form = MenuModelForm(instance=obj)  # 这个instance就是可以传入默认值
        return render(request, 'rbac/role_change.html', {'form': form})
    form = MenuModelForm(instance=obj, data=request.POST)
    if form.is_valid():
        form.save()
        url = memory_reverse(request, 'rbac:menu_list')
        return redirect(url)
    return render(request, 'rbac/role_change.html', {'form': form})


def menu_del(request, pk):
    url = memory_reverse(request, 'rbac:menu_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': url})
    models.Menu.objects.filter(pk=pk).delete()
    return redirect(url)


def second_menu_add(request, menu_id):
    '''
    添加二级菜单
    :param request:
    :param pk: 选中的默认一级菜单
    :return:
    '''

    menu_object = models.Menu.objects.filter(id=menu_id).first()
    if request.method == 'GET':
        form = SecondMenuModelForm(initial={'menu': menu_object})
        return render(request, 'rbac/role_change.html', {'form': form})

    form = SecondMenuModelForm(data=request.POST)

    if form.is_valid():
        form.save()
        url = memory_reverse(request, 'rbac:menu_list')
        return redirect(url)
    return render(request, 'rbac/role_change.html', {'form': form})


def second_menu_edit(request, pk):
    '''
    编辑二级菜单
    :param request:
    :param pk: 当即要编辑的二级菜单id
    :return:
    '''

    permission_object = models.Permission.objects.filter(id=pk).first()
    if request.method == 'GET':
        form = SecondMenuModelForm(instance=permission_object)
        return render(request, 'rbac/role_change.html', {'form': form})

    form = SecondMenuModelForm(data=request.POST, instance=permission_object)

    if form.is_valid():
        form.save()
        url = memory_reverse(request, 'rbac:menu_list')
        return redirect(url)
    return render(request, 'rbac/role_change.html', {'form': form})


def second_menu_del(request, pk):
    '''
    删除二级菜单
    :param request:
    :param pk: 当即要编辑的二级菜单id
    :return:
    '''

    url = memory_reverse(request, 'rbac:menu_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': url})
    models.Permission.objects.filter(pk=pk).delete()
    return redirect(url)


def permission_add(request, second_menu_id):
    if request.method == 'GET':
        form = PermissionModelForm()
        return render(request, 'rbac/role_change.html', {'form': form})

    form = PermissionModelForm(data=request.POST)

    if form.is_valid():
        second_menu_object = models.Permission.objects.filter(id=second_menu_id).first()
        if not second_menu_object:
            return HttpResponse('二级菜单不存在 请重新选择')
        # form.instance包含用户提交的所有值
        form.instance.pid = second_menu_object
        form.save()
        url = memory_reverse(request, 'rbac:menu_list')
        return redirect(url)
    return render(request, 'rbac/role_change.html', {'form': form})


def permission_edit(request, pk):
    permission_object = models.Permission.objects.filter(id=pk).first()
    if request.method == 'GET':
        form = PermissionModelForm(instance=permission_object)
        return render(request, 'rbac/role_change.html', {'form': form})

    form = PermissionModelForm(data=request.POST, instance=permission_object)

    if form.is_valid():
        form.save()
        url = memory_reverse(request, 'rbac:menu_list')
        return redirect(url)
    return render(request, 'rbac/role_change.html', {'form': form})


def permission_del(request, pk):
    url = memory_reverse(request, 'rbac:menu_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': url})
    models.Permission.objects.filter(pk=pk).delete()
    return redirect(url)


def multi_permissions(request):
    '''
    批量操作权限
    :param request:
    :return:
    '''

    post_type = request.GET.get('type')
    formset_add_class = formset_factory(MultiAddPermissionForm, extra=0)
    generate_formset = None
    update_formset = None

    update_formset_class = formset_factory(MultiEditPermissionForm, extra=0)

    if request.method == 'POST' and post_type == 'generate':
        formset = formset_add_class(data=request.POST)
        if formset.is_valid():
            object_list = []
            post_row_list = formset.cleaned_data
            has_error = False
            for i in range(0, formset.total_form_count()):
                row_dict = post_row_list[i]
                try:
                    new_object = models.Permission(**row_dict)
                    new_object.validate_unique()
                    object_list.append(new_object)
                except Exception as e:
                    formset.errors[i].update(e)
                    generate_formset = formset
                    has_error = True
            if not has_error:
                models.Permission.objects.bulk_create(object_list, batch_size=100)  # 批量添加
        else:
            generate_formset = formset
    if request.method == 'POST' and post_type == 'update':
        formset = update_formset_class(data=request.POST)
        if formset.is_valid():
            post_row_list = formset.cleaned_data

            for i in range(0, formset.total_form_count()):
                row_dict = post_row_list[i]
                permission_id = row_dict.pop('id')
                try:
                    row_object = models.Permission.objects.filter(id=permission_id).first()
                    for k, v in row_dict.items():
                        setattr(row_object, k, v)
                    row_object.validate_unique()
                    row_object.save()
                except Exception as e:
                    formset.errors[i].update(e)
                    update_formset = formset
        else:
            update_formset = formset
    # 获取项目中所有的URL
    all_url_dict = get_all_url_dict()
    router_name_set = set(all_url_dict.keys())

    # 2.获取数据库中所有的URL
    permissions = models.Permission.objects.all().values('id', 'title', 'name', 'url', 'pid_id', 'menu_id')
    permissions_dict = OrderedDict()
    permission_name_set = set()
    for row in permissions:
        permissions_dict[row['name']] = row
        permission_name_set.add(row['name'])

    for name, value in permissions_dict.items():
        router_row_dict = all_url_dict.get(name)
        if not router_row_dict:
            continue
        if value['url'] != router_row_dict['url']:
            value['url'] = '路由和数据库中不一致'

    # 3.应该添加，删除，修改的权限
    if not generate_formset:
        generate_name_list = router_name_set - permission_name_set
        generate_formset = formset_add_class(
            initial=[row_dict for name, row_dict in all_url_dict.items() if name in generate_name_list])
    delete_name_list = permission_name_set - router_name_set
    delete_row_list = [row_dict for name, row_dict in permissions_dict.items() if name in delete_name_list]
    if not update_formset:
        update_name_list = router_name_set & permission_name_set
        update_formset = update_formset_class(
            initial=[row_dict for name, row_dict in permissions_dict.items() if name in update_name_list])
    return render(request, 'rbac/multi_permissions.html', {
        'generate_formset': generate_formset,
        'delete_row_list': delete_row_list,
        'update_formset': update_formset})


def multi_permissions_del(request, pk):
    '''
    批量页面的权限删除
    :param request:
    :param pk:
    :return:
    '''
    url = memory_reverse(request, 'rbac:multi_permissions')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': url})
    models.Permission.objects.filter(pk=pk).delete()
    return redirect(url)


def distribute_permissions(request):

    user_id = request.GET.get('uid')
    user_model_class = import_string(settings.RBAC_USER_MODEL_CLASS)
    user_object = user_model_class.objects.filter(id=user_id).first()
    if not user_object:
        user_id = None

    role_id = request.GET.get('rid')
    role_object = models.Role.objects.filter(id=role_id).first()
    if not role_object:
        role_id = None

    if request.method == 'POST' and request.POST.get('type') == 'role':
        role_id_list = request.POST.getlist('roles')
        #用户和角色关系添加到第三张表(关系表)
        if not user_object:
            return HttpResponse('请选择用户')
        user_object.roles.set(role_id_list)
    if request.method == 'POST' and request.POST.get('type') == 'permission':
        permission_id_list = request.POST.getlist('permissions')
        if not role_object:
            return HttpResponse('请选择角色')
        role_object.permissions.set(permission_id_list)


    # 获取当前用户拥有的所有角色
    if user_id:
        user_has_roles = user_object.roles.all()
    else:
        user_has_roles = []

    user_has_roles_dict = {item.id: None for item in user_has_roles}

    # 获取当前用户拥有的所有权限
    # 如果选中的角色，优先显示选中角色所拥有的权限
    # 如果没有选择觉得，才显示用户所拥有的权限
    if role_object:  # 选择了角色
        user_has_permissions = role_object.permissions.all()
        user_has_permissions_dict = {item.id: None for item in user_has_permissions}
    elif user_id:
        user_has_permissions = user_object.roles.filter(permissions__id__isnull=False).values('permissions').distinct()
        user_has_permissions_dict = {item['permissions']: None for item in user_has_permissions}
    else:
        user_has_permissions = []
        user_has_permissions_dict = {}




    # 获取所有可显示的信息
    all_user_list = user_model_class.objects.all()

    all_role_list = models.Role.objects.all()

    menu_permission_list = []

    # 所有的菜单(一级菜单)
    all_menu_list = models.Menu.objects.values('id', 'title')
    # 所有的二级菜单
    all_second_menu_list = models.Permission.objects.filter(menu__isnull=False).values('id', 'title', 'menu_id')
    # 所有的权限
    all_permission_list = models.Permission.objects.filter(menu__isnull=True).values('id', 'title', 'pid_id')

    all_menu_dict = {}
    all_second_menu_dict = {}
    for item in all_menu_list:
        item['children'] = []
        all_menu_dict[item['id']] = item


    for row in all_second_menu_list:
        row['children'] = []
        all_second_menu_dict[row['id']] = row
        menu_id = row['menu_id']
        all_menu_dict[menu_id]['children'].append(row)

    for i in all_permission_list:
        pid = i['pid_id']
        if not pid:
            continue
        all_second_menu_dict[pid]['children'].append(i)

    return render(request, 'rbac/distribution_permissions.html',
                {'user_list': all_user_list,
                'role_list': all_role_list,
                'all_menu_dict': all_menu_list,
                'user_id': user_id,
                'role_id': role_id,
                'user_has_roles_dict': user_has_roles_dict,
                'user_has_permissions_dict': user_has_permissions_dict,
                })
