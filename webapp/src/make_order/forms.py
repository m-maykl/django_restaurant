from django import forms


class Order_form(forms.Form):
    point = forms.ChoiceField(choices = (('1','Київ'),('2','Одеса'),('3','Львів')))
    burger = forms.BooleanField(required=False)
    roll = forms.BooleanField(required=False)
    salad = forms.BooleanField(required=False)
    coca_cola = forms.BooleanField(required=False)
    ice_cream = forms.BooleanField(required=False)
    