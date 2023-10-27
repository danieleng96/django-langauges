from .models import Phonetics, Ipa_phonemes_audio_href
import django_filters
from django import forms
from django.db import models
import requests


class language_filter(django_filters.FilterSet):
    f = django_filters.CharFilter(method ='lang_filt', label='Input Language')
    class Meta:
        model = Phonetics
        fields = ['f']
        filter_overrides = {
            models.CharField: {
            'filter_class': django_filters.CharFilter,
            'extra': lambda x: {
            'widget': forms.TextInput(attrs = {'class': "form_control"})
        },},}
        
    def lang_filt(self, queryset, name, value):
        return queryset.filter(language__icontains = value)
        
        
        #basic search by all fields
class Phonetics_filter(django_filters.FilterSet):
    class Meta:
        model = Phonetics
        fields = ['language', 'segment_class', 'segment', 'representation_percent']