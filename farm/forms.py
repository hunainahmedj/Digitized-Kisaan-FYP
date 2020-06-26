from django import forms
from .models import Farm, Picture


class FarmForm(forms.ModelForm):

    farm_name = forms.CharField(
        label='Name',
        widget=forms.TextInput(
            attrs={
                "placeholder": "Name of Farm"
            }
        ))
    farm_area = forms.IntegerField(
        label='Area',
        widget=forms.TextInput(
            attrs={
                "placeholder": "Area of Farm in Sq"
            }
        ))

    class Meta:
        model = Farm
        fields = ['farm_name', 'farm_area',
                  'farm_country']


class FarmSearchForm(forms.Form):

    farm_lookup = forms.CharField(label='Farm Lookup ID', widget=forms.TextInput(
        attrs={
            "placeholder": "Lookup ID eg: Xqvy67!"
        }
    ))



class PictureForm(forms.ModelForm):

    class Meta:
        model = Picture
        fields = ['farm_id', 'resource_GRE',
                  'resource_NIR', 'resource_RED', 'resource_REG']
