#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
from django.template import Library
from django.conf import settings
from collections import OrderedDict
from django.urls import reverse
from django.http import QueryDict
from rbac.service import urls
register = Library()


@register.inclusion_tag('rbac/static_menu.html')
def static_menu(request):
    """
    创建一级菜单
    :return:
    """
    menu_list = request.session[settings.MENU_SESSION_KEY]
    return {'menu_list': menu_list}


@register.inclusion_tag('rbac/multi_menu.html')
def multi_menu(request):
    """
    创建二级菜单
    :return:
    """
    menu_dict = request.session[settings.MENU_SESSION_KEY]
    current_id = request.current_select_permission


    # 对字典的key进行排序
    key_list = sorted(menu_dict)

    # 空的有序字典
    ordered_dict = OrderedDict()

    for key in key_list:
        val = menu_dict[key]
        val['class'] = 'hide'

        for per in val['children']:
            if per['id'] == current_id:
                per['class'] = 'active'
                val['class'] = ''
        ordered_dict[key] = val

    return {'menu_dict': ordered_dict}

@register.inclusion_tag('rbac/breadcrumb.html')
def breadcrumb(request):
    url_record = request.url_record
    return {'url_record':url_record}

@register.filter
def has_permission(request,name):
    #最多有两个参数
    if name in request.session[settings.PERMISSION_SESSION_KEY]:
        return True

@register.simple_tag
def memory_url(request,name, *args, **kwargs):
    '''
    生成带有原搜索条件的URL（替代了原有的url)
    这里是发送过去 service.urls 是接受回来
    :param request:
    :param name:
    :return:
    '''
    basic_url = reverse(name,args=args,kwargs=kwargs)
    #该url无参数
    if not request.GET:
        return basic_url
    query_dict = QueryDict(mutable=True)
    query_dict['_filter'] = request.GET.urlencode() #_filter=mid=2&age=99
    return '%s?%s' %(basic_url,query_dict.urlencode())