import django_filters
from django import forms
from django_filters import FilterSet
from .models import *


class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'post_text': ['icontains'],
            'date_create': ['gt', 'lt'],

        }
        filter_overrides = {
            models.DateField: {
                'filter_class': django_filters.DateFilter,
                'extra': lambda f: {
                    'widget': forms.DateInput,
                },
            },
        }