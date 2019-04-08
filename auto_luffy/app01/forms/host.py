from django import forms
from app01 import models
from django.core.exceptions import ValidationError
from rbac.service.forms import BootStrapModelForm




class HostModelForm(BootStrapModelForm):

    class Meta:
        model = models.Host
        fields = '__all__'


class UpdateHostModelForm(BootStrapModelForm):
    class Meta:
        model = models.Host
        fields = '__all__'