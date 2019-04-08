from collections import OrderedDict
from django.conf import settings
from django.utils.module_loading import import_string
from django.urls import URLPattern, URLResolver
import re

def check_url_exclude(url):

    for item in settings.VALID_URL_LIST:
        if re.match(item, url):
            return True

def recursion_url(pre_namespace, pre_url, url_patterns, url_ordered_dict):
    '''
    递归的去获取URL
    :param pre_namespace:namespace前缀，以后用于拼接name
    :param pre_url:url前缀，用于拼接URL
    :param url_patterns:路由关系列表
    :param url_ordered_dict:用于保存递归中获取的所有路由
    :return:
    '''
    for item in url_patterns:
        if isinstance(item, URLPattern):  # 非路由分发
            if not item.name:
                continue
            if pre_namespace:
                name = '%s:%s' % (pre_namespace, item.name)
            else:
                name = item.name

            url = pre_url + str(item.pattern)  # /^rbac/^user/edit
            url = url.replace('^', '').replace('$', '')
            if check_url_exclude(url):
                continue
            url_ordered_dict[name] = {'name': name, 'url': url}
        elif isinstance(item, URLResolver):  # 路由分发，进行递归操作
            if pre_namespace:
                if item.namespace:
                    namespace = '%s:%s' % (pre_namespace, item.namespace)
                else:
                    namespace = item.namespace
            else:
                if item.namespace:
                    namespace = item.namespace
                else:
                    namespace = None
            recursion_url(namespace, pre_url + str(item.pattern), item.url_patterns, url_ordered_dict)


def get_all_url_dict():
    '''
    获取项目中所有的URL（必须有name别名）
    :return:
    '''
    url_ordered_dict = OrderedDict()
    md = import_string(settings.ROOT_URLCONF) #建立一个模块取值
    recursion_url(None, '/', md.urlpatterns, url_ordered_dict)  # 递归的去取值
    return url_ordered_dict