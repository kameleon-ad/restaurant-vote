from django import forms


class EmployeeForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    email = forms.EmailField()
