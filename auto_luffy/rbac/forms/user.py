from rbac import models
from django import forms
from django.core.exceptions import ValidationError
from rbac.service.forms import BootStrapModelForm


class UserModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(label='确认密码')

    class Meta:
        model = models.UserInfo
        fields = ['name', 'email', 'password', 'confirm_password']
        error_messages = {
            'name': {'required': '用户名不能为空'},
            'email': {'required': '邮箱不能为空'},
            'password': {'required': '密码不能为空'},
            'confirm_password': {'required': '确认密码不能为空'},
        }


    def clean_confirm_password(self):
        '''
        检测密码是否一致
        :return:
        '''
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise ValidationError('两次密码数据不一致')
        return confirm_password


class UpdateUserModelForm(BootStrapModelForm):
    class Meta:
        model = models.UserInfo
        fields = ['name', 'email', ]
        error_messages = {
            'name': {'required': '用户名不能为空'},
            'email': {'required': '邮箱不能为空'},
        }



class ResetUserModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(label='确认密码')

    class Meta:
        model = models.UserInfo
        fields = ['password', 'confirm_password',]
        error_messages = {
            'confirm_password': {'required': '确认密码不能为空'},
            'password': {'required': '密码不能为空'},
        }


    def clean_confirm_password(self):
        '''
        检测密码是否一致
        :return:
        '''
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise ValidationError('两次密码数据不一致')
        return confirm_password
