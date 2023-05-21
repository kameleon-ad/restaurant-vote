from django import forms


class VoteMenuFormV1(forms.Form):
    menu_id = forms.IntegerField()
