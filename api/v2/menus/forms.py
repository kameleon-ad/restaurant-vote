from django import forms


class VoteMenuFormV2(forms.Form):
    votes = forms.JSONField()
