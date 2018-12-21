from django import forms
from users.models import *

class AddUser(forms.ModelForm):
    class Meta:
        model =  UserProfile
        widgets = {
            'password': forms.PasswordInput,
        }
        fields = [
            'username',
            'password',
            'email',
            'is_teacher',
            'is_site_admin',
        ]

class EditUserByUser(forms.ModelForm):
    class Meta:
        model = UserProfile
        widgets = {
            'password': forms.PasswordInput,
        }
        fields = [
            'username',
            'email',
            'password',
        ]
        # Dont want to modify blank setting inside module(doing so will break validation in admin site)
        # The redefined constructor won't harm any functionality
        def __init__(self, *args, **kwargs):
            super(EditUser, self).__init__(*args, **kwargs)

            for key in self.fields:
                self.fields[key].required = False

class EditUserByAdmin(EditUserByUser):
    class Meta(EditUserByUser.Meta):
        fields = EditUserByUser.Meta.fields + ['is_teacher', 'is_site_admin']

class Contact(forms.Form):
    sender = forms.CharField(label='Name', max_length=30)
    subject = forms.CharField(label='Subject', max_length=30)
    email = forms.EmailField(label='Email', max_length=30)
    message = forms.CharField(widget=forms.Textarea)