# forms.py - Formulaires personnalisés pour l'admin Django
from django import forms
from .models import ChurchBiography, ChurchConsistory, Contact
from .widgets import ServiceTimesWidget


class ChurchBiographyForm(forms.ModelForm):
    """Formulaire personnalisé pour ChurchBiography avec widget service_times"""
    
    class Meta:
        model = ChurchBiography
        fields = '__all__'
        widgets = {
            'service_times': ServiceTimesWidget(),
        }


class ChurchConsistoryForm(forms.ModelForm):
    """Formulaire personnalisé pour ChurchConsistory"""
    
    class Meta:
        model = ChurchConsistory
        fields = '__all__'


class ContactForm(forms.ModelForm):
    """Formulaire pour les messages de contact"""
    
    class Meta:
        model = Contact
        fields = '__all__'
