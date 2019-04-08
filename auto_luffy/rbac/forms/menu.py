from django import forms
from rbac import models
from django.utils.safestring import mark_safe
from rbac.service.forms import BootStrapModelForm
class MenuModelForm(forms.ModelForm):
    #radioselect意思就是变成单选框
    class Meta:
        model = models.Menu
        fields = '__all__'
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'icon':forms.RadioSelect(choices=[
                ['fa-superpowers',mark_safe('<i class="fa fa-superpowers" aria-hidden="true"></i>')],
                ['fa-thermometer-full', mark_safe('<i class="fa fa-thermometer-full" aria-hidden="true"></i>')],#x1就变成radio里面的value，xx1就变成显示的值
            ])
        }


class SecondMenuModelForm(BootStrapModelForm):
    #radioselect意思就是变成单选框
    class Meta:
        model = models.Permission
        exclude = ['pid']

class PermissionModelForm(BootStrapModelForm):
    class Meta:
        model = models.Permission
        fields = ['title','name', 'url']

class MultiAddPermissionForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form_control'
        })
    )
    url = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form_control'
        })
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form_control'
        })
    )
    menu_id = forms.ChoiceField(
        choices=[(None, '-----')],
        widget=forms.Select(attrs={
            'class': 'form_control'
        }),
        required=False
    )
    pid_id = forms.ChoiceField(
        choices=[(None, '-----')],
        widget=forms.Select(attrs={
            'class': 'form_control'
        }),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['menu_id'].choices += models.Menu.objects.values_list('id', 'title')
        self.fields['pid_id'].choices += models.Permission.objects.filter(pid__isnull=True).exclude(
            menu__isnull=True).values_list('id', 'title')


class MultiEditPermissionForm(forms.Form):
    id = forms.IntegerField(
        widget=forms.HiddenInput()
    )
    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form_control'
        })
    )
    url = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form_control'
        })
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form_control'
        })
    )
    menu_id = forms.ChoiceField(
        choices=[(None, '-----')],
        widget=forms.Select(attrs={
            'class': 'form_control'
        }),
        required=False
    )
    pid_id = forms.ChoiceField(
        choices=[(None, '-----')],
        widget=forms.Select(attrs={
            'class': 'form_control'
        }),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['menu_id'].choices += models.Menu.objects.values_list('id', 'title')
        self.fields['pid_id'].choices += models.Permission.objects.filter(pid__isnull=True).exclude(
            menu__isnull=True).values_list('id', 'title')
