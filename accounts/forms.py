from django import forms
from django.contrib.auth.models import User

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
            'password': forms.TextInput(attrs={'class': 'w-full px-3 py-1 rounded text-sm',
                                                 'autocomplete': 'off',
                                                 'required': True,
                                                'type': 'password',
                                                 }),
        }

