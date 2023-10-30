
import django_filters
from Myapp.models import *
from django import forms


class FarmFilter(django_filters.FilterSet):
    # level = django_filters.MultipleChoiceFilter(choices=Student.LevelChoices.choices,
    # widget = forms.CheckboxSelectMultiple)
    class Meta:
        model = Product
        
        fields = {
            'name' : ['icontains'],
            'location' : ['exact'],
            'status' : ['exact'],
            'choice' :['exact'],
            #'department' :['exact']
        }