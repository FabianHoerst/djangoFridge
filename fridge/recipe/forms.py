from django import forms
from .models import IngredientInput

class IngredientInputForm(forms.ModelForm):
    class Meta:
        model = IngredientInput
        fields = ('input_string',)

