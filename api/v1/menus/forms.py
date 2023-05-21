from django import forms


class VoteMenuForm(forms.Form):
    votes = forms.JSONField()
