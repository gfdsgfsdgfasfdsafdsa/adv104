from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full px-3 py-1 rounded text-sm',
                                                 'autocomplete': 'off',
                                                 'required': True
                                                 }),
            'last_name': forms.TextInput(attrs={'class': 'w-full px-3 py-1 rounded text-sm',
                                                'autocomplete': 'off',
                                                'required': True
                                                }),
            'email': forms.TextInput(attrs={'class': 'w-full px-3 py-1 rounded text-sm',
                                            'autocomplete': 'off',
                                            'required': True
                                            }),
        }


class UserPasswordForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['password']

        widgets = {
            'password': forms.TextInput(attrs={'class': 'w-full px-3 py-1 rounded text-sm', 'autocomplete': 'off',
                                               'required': True, 'type': 'password'}),
        }


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, error_messages={'invalid': 'Email already exist.'})
    first_name = forms.CharField(max_length=100, required=True, error_messages={'required': 'Firstname is required.'})
    last_name = forms.CharField(max_length=100, required=True, error_messages={'required': 'Lastname is required.'})

    class Meta:
        model = User
        fields = ["email", "username", "first_name", "last_name", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['class'] = 'w-full px-3 py-1 rounded text-sm'
        self.fields['email'].widget.attrs['autocomplete'] = 'off'

        self.fields['username'].widget.attrs['class'] = 'w-full px-3 py-1 rounded text-sm'
        self.fields['username'].widget.attrs['autocomplete'] = 'off'

        self.fields['last_name'].widget.attrs['class'] = 'w-full px-3 py-1 rounded text-sm'
        self.fields['last_name'].widget.attrs['autocomplete'] = 'off'

        self.fields['first_name'].widget.attrs['class'] = 'w-full px-3 py-1 rounded text-sm'
        self.fields['first_name'].widget.attrs['autocomplete'] = 'off'

        self.fields['password1'].widget.attrs['class'] = 'w-full px-3 py-1 rounded text-sm'
        self.fields['password2'].widget.attrs['class'] = 'w-full px-3 py-1 rounded text-sm'

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


