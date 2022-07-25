from .models import User
from django import forms
from django.forms import ModelForm


class UserForm(forms.ModelForm):
    # password = forms.CharField(required=True, max_length=128, widget=forms.PasswordInput())
    # confirm_password = forms.CharField(required=True, max_length=128, widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'user_type', 'roles', 'groups']
        exclude = ['is_active', 'is_superuser', 'is_staff', 'date_joined', 'last_login']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if visible.name == 'groups':
                visible.field.widget.attrs['required'] = False
            else:
                visible.field.widget.attrs['required'] = True


class UserRoleForm(forms.ModelForm):
    username = forms.ModelChoiceField(queryset=User.objects.filter(user_type=3).values_list('username', flat=True), to_field_name='username')

    class Meta:
        model = User
        fields = ['username', 'roles']

    def __init__(self, *args, **kwargs):
        super(UserRoleForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['required'] = True
