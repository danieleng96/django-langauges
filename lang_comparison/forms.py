from django import forms
import models
from crispy_forms.helper import FormHelper

required = 'This field is required'

class SearchLang(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
    class Meta:
        model = models.Phonetics
        fields = ['language']
