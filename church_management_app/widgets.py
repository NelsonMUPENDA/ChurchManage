# widgets.py - Widgets personnalisés pour les formulaires Django
from django import forms


class ServiceTimesWidget(forms.MultiWidget):
    """
    Widget personnalisé pour gérer les horaires de service de l'église.
    Permet de saisir plusieurs créneaux horaires (jour, heure début, heure fin).
    """
    
    def __init__(self, attrs=None):
        days = [
            ('', 'Choisir un jour'),
            ('monday', 'Lundi'),
            ('tuesday', 'Mardi'),
            ('wednesday', 'Mercredi'),
            ('thursday', 'Jeudi'),
            ('friday', 'Vendredi'),
            ('saturday', 'Samedi'),
            ('sunday', 'Dimanche'),
        ]
        
        widgets = (
            forms.Select(attrs={'class': 'form-select'}, choices=days),
            forms.TimeInput(attrs={'class': 'form-control', 'type': 'time', 'placeholder': 'Heure début'}),
            forms.TimeInput(attrs={'class': 'form-control', 'type': 'time', 'placeholder': 'Heure fin'}),
        )
        super().__init__(widgets, attrs)
    
    def decompress(self, value):
        """
        Décompresse la valeur JSON en liste de valeurs pour chaque sous-widget.
        """
        if value:
            if isinstance(value, dict):
                return [
                    value.get('day', ''),
                    value.get('start_time', ''),
                    value.get('end_time', '')
                ]
            elif isinstance(value, str):
                # Essayer de parser la chaîne
                try:
                    import json
                    data = json.loads(value)
                    return [
                        data.get('day', ''),
                        data.get('start_time', ''),
                        data.get('end_time', '')
                    ]
                except (json.JSONDecodeError, ValueError):
                    return ['', '', '']
        return ['', '', '']
    
    def value_from_datadict(self, data, files, name):
        """
        Combine les valeurs des sous-widgets en une valeur JSON.
        """
        day = data.get(name + '_0', '')
        start_time = data.get(name + '_1', '')
        end_time = data.get(name + '_2', '')
        
        if day or start_time or end_time:
            import json
            return json.dumps({
                'day': day,
                'start_time': start_time,
                'end_time': end_time,
            })
        return ''
    
    def format_output(self, rendered_widgets):
        """
        Formate l'affichage des sous-widgets.
        """
        return (
            '<div class="service-time-widget">'
            '<div class="row g-2">'
            '<div class="col-md-4">' + rendered_widgets[0] + '</div>'
            '<div class="col-md-4">' + rendered_widgets[1] + '</div>'
            '<div class="col-md-4">' + rendered_widgets[2] + '</div>'
            '</div>'
            '</div>'
        )


class JSONFieldWidget(forms.Textarea):
    """
    Widget pour afficher et éditer des champs JSON de manière formatée.
    """
    
    def __init__(self, attrs=None):
        default_attrs = {
            'class': 'form-control vLargeTextField',
            'rows': 10,
            'style': 'font-family: monospace;',
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)
    
    def format_value(self, value):
        """
        Formate la valeur JSON pour l'affichage.
        """
        if value is None:
            return ''
        try:
            import json
            if isinstance(value, str):
                # Parser et re-formater proprement
                data = json.loads(value)
                return json.dumps(data, indent=2, ensure_ascii=False)
            elif isinstance(value, (dict, list)):
                return json.dumps(value, indent=2, ensure_ascii=False)
        except (json.JSONDecodeError, ValueError, TypeError):
            pass
        return str(value)


class ColorPickerWidget(forms.TextInput):
    """
    Widget de sélection de couleur HTML5.
    """
    
    input_type = 'color'
    template_name = 'django/forms/widgets/text.html'
    
    def __init__(self, attrs=None):
        default_attrs = {'class': 'form-control form-control-color'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)


class PhoneNumberWidget(forms.TextInput):
    """
    Widget pour la saisie de numéros de téléphone avec masque.
    """
    
    def __init__(self, attrs=None):
        default_attrs = {
            'class': 'form-control',
            'placeholder': '+243 ...',
            'pattern': r'[\+]?[0-9\s\-\(\)\.]+',
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)
