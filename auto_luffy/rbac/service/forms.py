from django import forms



class BootStrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BootStrapModelForm, self).__init__(*args, **kwargs)  # 执行父类的构造函数
        # 统一给modelform加上样式
        for name, field in self.fields.items():  # 循环出所有的字段
            field.widget.attrs['class'] = 'form-control'