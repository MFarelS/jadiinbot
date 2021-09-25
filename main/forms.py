from django import forms

class IndexLoginForm(forms.Form):
    username = forms.CharField(max_length = 12)
    password = forms.CharField(max_length = 20)


class RegisterForm(forms.Form):
    username = forms.CharField(max_length = 12)
    password = forms.CharField(max_length = 20)
    confirm_password = forms.CharField(max_length = 20)
