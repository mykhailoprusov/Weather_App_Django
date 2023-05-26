from django import forms




class CityForm(forms.Form):

    city1 = forms.CharField(max_length=30, label="First City", required=True)
    city2 = forms.CharField(max_length=30, label="Second City", required=False)