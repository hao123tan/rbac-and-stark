
from django.urls import reverse
from django.http import QueryDict



def memory_reverse(request,name,*args,**kwargs):
    '''
    反向生成带参数的url
        1.在url这种将原来搜索条件,如mid后面的值
        2.reverse 生成原来的URL，如/menu/list/
        3./menu/list/?mid%3D2

    示例:
        http://127.0.0.1:8000/rbac/menu/list/?mid=3
    :param request:
    :param name:
    :param args:
    :param kwargs:
    :return:
    '''
    url = reverse(name,args=args,kwargs=kwargs)
    original_params = request.GET.get('_filter')
    if original_params:
        url = '%s?%s' % (url, original_params)
    return url


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