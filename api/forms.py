from django import forms

class GetUserBySessionForm(forms.Form):
    session_key = forms.CharField(max_length = 255)