from django import forms
from listing.models import Category

class SearchForm(forms.Form):
    q = forms.CharField(
        label='Rechercher',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Que recherchez-vous ?'
        })
    )
    
    location = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Localisation'
        })
    )
    
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="Toutes les catégories",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tags (séparés par des virgules)'
        })
    ) 