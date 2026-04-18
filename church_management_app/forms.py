# forms.py - Formulaires pour l'application Django traditionnelle
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import (
    ChurchBiography, ChurchConsistory, Contact,
    Member, Family, HomeGroup, Department, Ministry,
    Event, Attendance, BaptismEvent, BaptismCandidate,
    EvangelismActivity, TrainingEvent, MarriageRecord,
    FinancialCategory, FinancialTransaction,
    Announcement, AnnouncementDeck, AnnouncementDeckItem,
    Document, LogisticsItem, ChurchSettings,
    EventAttendanceAggregate
)
from .widgets import ServiceTimesWidget

User = get_user_model()


# ============================================================
# Formulaires d'Authentification
# ============================================================

class LoginForm(AuthenticationForm):
    """Formulaire de connexion personnalisé"""
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nom d\'utilisateur',
            'id': 'id_username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mot de passe',
            'id': 'id_password'
        })
    )


class UserCreateForm(UserCreationForm):
    """Formulaire de création d'utilisateur"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    photo = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'role', 'phone', 'photo', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    """Formulaire de mise à jour d'utilisateur (avec role - pour admins)"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        max_length=30, 
        required=True,
        label='Prénom',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=30, 
        required=True,
        label='Nom',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    phone = forms.CharField(
        max_length=20, 
        required=False,
        label='Téléphone',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    photo = forms.ImageField(
        required=False,
        label='Photo de profil',
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        required=True,
        label='Rôle',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'photo', 'role']


class ProfileUpdateForm(forms.ModelForm):
    """Formulaire d'édition de son propre profil (sans role)"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        max_length=30, 
        required=True,
        label='Prénom',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=30, 
        required=True,
        label='Nom',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    phone = forms.CharField(
        max_length=20, 
        required=False,
        label='Téléphone',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    photo = forms.ImageField(
        required=False,
        label='Photo de profil',
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'photo']


class PasswordChangeCustomForm(forms.Form):
    """Formulaire de changement de mot de passe"""
    current_password = forms.CharField(
        label='Mot de passe actuel',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mot de passe actuel'
        })
    )
    new_password = forms.CharField(
        label='Nouveau mot de passe',
        min_length=8,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nouveau mot de passe'
        })
    )
    confirm_password = forms.CharField(
        label='Confirmer le mot de passe',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmer le mot de passe'
        })
    )
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
    
    def clean_current_password(self):
        current = self.cleaned_data.get('current_password')
        if not self.user.check_password(current):
            raise forms.ValidationError('Le mot de passe actuel est incorrect.')
        return current
    
    def clean(self):
        cleaned_data = super().clean()
        new = cleaned_data.get('new_password')
        confirm = cleaned_data.get('confirm_password')
        if new and confirm and new != confirm:
            raise forms.ValidationError('Les mots de passe ne correspondent pas.')
        return cleaned_data
    
    def save(self):
        self.user.set_password(self.cleaned_data['new_password'])
        self.user.save()
        return self.user


# ============================================================
# Formulaires pour les Membres
# ============================================================

class MemberForm(forms.ModelForm):
    """Formulaire pour créer/modifier un membre avec données User"""
    # Champs User
    first_name = forms.CharField(max_length=30, required=True, label='Prénom',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, label='Nom',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=False, label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone_country_code = forms.ChoiceField(
        required=False,
        label='Code pays',
        choices=[
            ('+243', '+243 (RDC)'),
            ('+250', '+250 (Rwanda)'),
            ('+257', '+257 (Burundi)'),
            ('+243', '+243 (Congo)'),
            ('+33', '+33 (France)'),
            ('+32', '+32 (Belgique)'),
            ('+1', '+1 (USA/Canada)'),
        ],
        initial='+243',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    phone = forms.CharField(max_length=20, required=False, label='Téléphone',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 0991234567'}))
    photo = forms.ImageField(required=False, label='Photo',
        widget=forms.FileInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Member
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'photo',
            'birth_date', 'place_of_birth', 'gender', 'nationality',
            'marital_status', 'occupation', 'public_function', 'church_position',
            'education_level', 'father_full_name', 'mother_full_name',
            'province', 'city', 'commune', 'quarter', 'avenue', 'house_number',
            'emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relation',
            'baptism_date', 'family', 'department', 'ministry',
            'is_active', 'inactive_reason'
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'baptism_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'place_of_birth': forms.TextInput(attrs={'class': 'form-control'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control'}),
            'marital_status': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Célibataire, Marié(e), Divorcé(e)...'}),
            'occupation': forms.TextInput(attrs={'class': 'form-control'}),
            'public_function': forms.TextInput(attrs={'class': 'form-control'}),
            'church_position': forms.TextInput(attrs={'class': 'form-control'}),
            'education_level': forms.TextInput(attrs={'class': 'form-control'}),
            'father_full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'province': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'commune': forms.TextInput(attrs={'class': 'form-control'}),
            'quarter': forms.TextInput(attrs={'class': 'form-control'}),
            'avenue': forms.TextInput(attrs={'class': 'form-control'}),
            'house_number': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_name': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_contact_relation': forms.TextInput(attrs={'class': 'form-control'}),
            'family': forms.Select(attrs={'class': 'form-select', 'id': 'family_select'}),
            'department': forms.Select(attrs={'class': 'form-select', 'id': 'department_select'}),
            'ministry': forms.Select(attrs={'class': 'form-select', 'id': 'ministry_select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'is_active_check'}),
            'inactive_reason': forms.Select(attrs={'class': 'form-select', 'id': 'inactive_reason_select'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pré-remplir les champs User si modification
        if self.instance and self.instance.pk and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
            self.fields['phone'].initial = self.instance.user.phone
        
        # Filtrer les options de genre pour exclure 'Other'
        self.fields['gender'].choices = [
            ('', '---------'),
            ('M', 'Masculin'),
            ('F', 'Féminin'),
        ]
    
    def save(self, commit=True):
        member = super().save(commit=False)
        
        # Créer ou mettre à jour l'utilisateur
        if not member.pk or not member.user:
            # Création : nouvel utilisateur
            user = User.objects.create(
                username=self.cleaned_data['email'] or f"member_{Member.objects.count() + 1}",
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                email=self.cleaned_data['email'] or '',
                phone=self.cleaned_data['phone'] or '',
            )
            if self.cleaned_data.get('photo'):
                user.photo = self.cleaned_data['photo']
                user.save()
            member.user = user
        else:
            # Modification : mettre à jour l'utilisateur existant
            user = member.user
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email'] or ''
            user.phone = self.cleaned_data['phone'] or ''
            if self.cleaned_data.get('photo'):
                user.photo = self.cleaned_data['photo']
            user.save()
        
        if commit:
            member.save()
            self.save_m2m()
        
        return member


class FamilyForm(forms.ModelForm):
    """Formulaire pour créer/modifier une famille"""
    
    class Meta:
        model = Family
        fields = ['name', 'address', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }


class HomeGroupForm(forms.ModelForm):
    """Formulaire pour créer/modifier un groupe de maison"""
    
    class Meta:
        model = HomeGroup
        fields = ['name', 'leader', 'meeting_day', 'meeting_time', 'location']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'leader': forms.Select(attrs={'class': 'form-select'}),
            'meeting_day': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Samedi'}),
            'meeting_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'location': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class DepartmentForm(forms.ModelForm):
    """Formulaire pour créer/modifier un département"""
    
    class Meta:
        model = Department
        fields = ['name', 'description', 'head']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'head': forms.Select(attrs={'class': 'form-select'}),
        }


class MinistryForm(forms.ModelForm):
    """Formulaire pour créer/modifier un ministère"""
    
    class Meta:
        model = Ministry
        fields = ['name', 'description', 'leader']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'leader': forms.Select(attrs={'class': 'form-select'}),
        }


# ============================================================
# Formulaires pour les Événements
# ============================================================

class EventForm(forms.ModelForm):
    """Formulaire complet pour créer/modifier un événement"""
    
    class Meta:
        model = Event
        fields = [
            'title', 'description', 'event_type', 'duration_type', 'date', 'time',
            'location', 'moderator', 'preacher', 'choir', 'protocol_team',
            'tech_team', 'communicator', 'responsible', 'department',
            'poster_image', 'is_published', 'is_alert', 'alert_message'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre de l\'événement'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Description détaillée...'}),
            'event_type': forms.Select(attrs={'class': 'form-select'}),
            'duration_type': forms.Select(attrs={'class': 'form-select'}, choices=Event.DURATION_CHOICES),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lieu de l\'événement'}),
            'moderator': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Modérateur'}),
            'preacher': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prédicateur / Orateur'}),
            'choir': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Chorale / Groupe de louange'}),
            'protocol_team': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Équipe de protocole'}),
            'tech_team': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Équipe technique'}),
            'communicator': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Communicateur / MC'}),
            'responsible': forms.Select(attrs={'class': 'form-select'}),
            'department': forms.Select(attrs={'class': 'form-select'}),
            'poster_image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_alert': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'alert_message': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Message d\'alerte (si urgent)'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Rendre les champs optionnels vides par défaut
        self.fields['responsible'].empty_label = "-- Sélectionner un responsable --"
        self.fields['department'].empty_label = "-- Sélectionner un département --"
        self.fields['responsible'].queryset = Member.objects.filter(is_active=True)
        self.fields['department'].queryset = Department.objects.all()


class AttendanceForm(forms.ModelForm):
    """Formulaire pour marquer la présence"""
    
    class Meta:
        model = Attendance
        fields = ['event', 'member', 'attended']
        widgets = {
            'event': forms.Select(attrs={'class': 'form-select'}),
            'member': forms.Select(attrs={'class': 'form-select'}),
            'attended': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class BaptismEventForm(forms.ModelForm):
    """Formulaire pour créer un événement de baptême"""
    
    class Meta:
        model = BaptismEvent
        fields = ['event', 'executors']
        widgets = {
            'event': forms.Select(attrs={'class': 'form-select'}),
            'executors': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Liste des exécuteurs (JSON)'}),
        }


class BaptismCandidateForm(forms.ModelForm):
    """Formulaire pour ajouter un candidat au baptême"""
    
    class Meta:
        model = BaptismCandidate
        fields = ['baptism_event', 'name', 'post_name', 'address', 'phone_number', 'place_of_birth', 'birth_date', 'passport_photo']
        widgets = {
            'baptism_event': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'post_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'place_of_birth': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'passport_photo': forms.FileInput(attrs={'class': 'form-control'}),
        }


# ============================================================
# Formulaires pour l'Évangélisation
# ============================================================

class EvangelismActivityForm(forms.ModelForm):
    """Formulaire pour créer/modifier une activité d'évangélisation"""
    
    class Meta:
        model = EvangelismActivity
        fields = ['title', 'activity_type', 'custom_activity_type', 'date', 'time', 'location', 'moderator', 'published_event']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'activity_type': forms.Select(attrs={'class': 'form-select'}),
            'custom_activity_type': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'moderator': forms.TextInput(attrs={'class': 'form-control'}),
            'published_event': forms.Select(attrs={'class': 'form-select'}),
        }


class TrainingEventForm(forms.ModelForm):
    """Formulaire pour créer/modifier une formation"""
    
    class Meta:
        model = TrainingEvent
        fields = ['title', 'date', 'time', 'location', 'trainer', 'lesson', 'published_event']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'trainer': forms.TextInput(attrs={'class': 'form-control'}),
            'lesson': forms.TextInput(attrs={'class': 'form-control'}),
            'published_event': forms.Select(attrs={'class': 'form-select'}),
        }


# ============================================================
# Formulaires pour les Mariages
# ============================================================

class MarriageRecordForm(forms.ModelForm):
    """Formulaire pour créer/modifier un registre de mariage"""
    
    class Meta:
        model = MarriageRecord
        fields = [
            'groom', 'bride', 'groom_full_name', 'bride_full_name',
            'groom_birth_date', 'groom_birth_place', 'groom_nationality', 'groom_passport_photo',
            'bride_birth_date', 'bride_birth_place', 'bride_nationality', 'bride_passport_photo',
            'godfather_full_name', 'godfather_nationality', 'godfather_passport_photo',
            'godmother_full_name', 'godmother_nationality', 'godmother_passport_photo',
            'planned_date', 'planned_time', 'location',
            'dowry_paid', 'civil_verified', 'prenuptial_tests', 'approved',
            'published_event'
        ]
        widgets = {
            'groom': forms.Select(attrs={'class': 'form-select'}),
            'bride': forms.Select(attrs={'class': 'form-select'}),
            'groom_full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'bride_full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'groom_birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'groom_birth_place': forms.TextInput(attrs={'class': 'form-control'}),
            'groom_nationality': forms.TextInput(attrs={'class': 'form-control'}),
            'groom_passport_photo': forms.FileInput(attrs={'class': 'form-control'}),
            'bride_birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'bride_birth_place': forms.TextInput(attrs={'class': 'form-control'}),
            'bride_nationality': forms.TextInput(attrs={'class': 'form-control'}),
            'bride_passport_photo': forms.FileInput(attrs={'class': 'form-control'}),
            'godfather_full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'godfather_nationality': forms.TextInput(attrs={'class': 'form-control'}),
            'godfather_passport_photo': forms.FileInput(attrs={'class': 'form-control'}),
            'godmother_full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'godmother_nationality': forms.TextInput(attrs={'class': 'form-control'}),
            'godmother_passport_photo': forms.FileInput(attrs={'class': 'form-control'}),
            'planned_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'planned_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'dowry_paid': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'civil_verified': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'prenuptial_tests': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'approved': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'published_event': forms.Select(attrs={'class': 'form-select'}),
        }


# ============================================================
# Formulaires pour les Finances
# ============================================================

class FinancialCategoryForm(forms.ModelForm):
    """Formulaire pour créer/modifier une catégorie financière"""
    
    class Meta:
        model = FinancialCategory
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


class FinancialTransactionForm(forms.ModelForm):
    """Formulaire pour créer/modifier une transaction financière"""
    DIRECTION_CHOICES = [
        ('in', 'Entrée'),
        ('out', 'Sortie'),
    ]
    
    direction = forms.ChoiceField(
        choices=DIRECTION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    class Meta:
        model = FinancialTransaction
        fields = ['date', 'category', 'direction', 'amount', 'transaction_type', 'reference_number', 'member', 'event']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
            'transaction_type': forms.Select(attrs={'class': 'form-select'}),
            'reference_number': forms.TextInput(attrs={'class': 'form-control'}),
            'member': forms.Select(attrs={'class': 'form-select'}),
            'event': forms.Select(attrs={'class': 'form-select'}),
        }


# ============================================================
# Formulaires pour les Annonces
# ============================================================

class AnnouncementForm(forms.ModelForm):
    """Formulaire pour créer/modifier une annonce"""
    
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'image', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class AnnouncementDeckForm(forms.ModelForm):
    """Formulaire pour créer/modifier un deck d'annonces"""
    
    class Meta:
        model = AnnouncementDeck
        fields = ['title', 'event', 'header_text', 'theme_text', 'pptx_file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'event': forms.Select(attrs={'class': 'form-select'}),
            'header_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'theme_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'pptx_file': forms.FileInput(attrs={'class': 'form-control'}),
        }


class AnnouncementDeckItemForm(forms.ModelForm):
    """Formulaire pour ajouter un élément à un deck"""
    
    class Meta:
        model = AnnouncementDeckItem
        fields = ['deck', 'text', 'order']
        widgets = {
            'deck': forms.Select(attrs={'class': 'form-select'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }


# ============================================================
# Formulaires pour les Documents et Logistique
# ============================================================

class DocumentForm(forms.ModelForm):
    """Formulaire pour uploader un document"""
    
    class Meta:
        model = Document
        fields = ['title', 'document_type', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'document_type': forms.Select(attrs={'class': 'form-select'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }


class LogisticsItemForm(forms.ModelForm):
    """Formulaire pour créer/modifier un élément logistique"""
    
    class Meta:
        model = LogisticsItem
        fields = ['name', 'category', 'quantity', 'unit', 'location', 'condition', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'unit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: pièces, litres'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'condition': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


# ============================================================
# Formulaires pour l'Église (déjà existants)
# ============================================================

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


class ChurchSettingsForm(forms.ModelForm):
    """Formulaire pour les paramètres de l'église"""
    
    class Meta:
        model = ChurchSettings
        fields = [
            'church_name', 'church_slogan', 'logo', 'favicon',
            'address', 'city', 'country',
            'phone_primary', 'phone_secondary', 'email_primary', 'email_secondary',
            'office_hours_weekdays', 'office_hours_saturday', 'office_hours_sunday',
            'facebook_url', 'youtube_url', 'instagram_url', 'twitter_url', 'whatsapp_number', 'telegram_url'
        ]
        widgets = {
            'church_name': forms.TextInput(attrs={'class': 'form-control'}),
            'church_slogan': forms.TextInput(attrs={'class': 'form-control'}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
            'favicon': forms.FileInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_primary': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_secondary': forms.TextInput(attrs={'class': 'form-control'}),
            'email_primary': forms.EmailInput(attrs={'class': 'form-control'}),
            'email_secondary': forms.EmailInput(attrs={'class': 'form-control'}),
            'office_hours_weekdays': forms.TextInput(attrs={'class': 'form-control'}),
            'office_hours_saturday': forms.TextInput(attrs={'class': 'form-control'}),
            'office_hours_sunday': forms.TextInput(attrs={'class': 'form-control'}),
            'facebook_url': forms.URLInput(attrs={'class': 'form-control'}),
            'youtube_url': forms.URLInput(attrs={'class': 'form-control'}),
            'instagram_url': forms.URLInput(attrs={'class': 'form-control'}),
            'twitter_url': forms.URLInput(attrs={'class': 'form-control'}),
            'whatsapp_number': forms.TextInput(attrs={'class': 'form-control'}),
            'telegram_url': forms.URLInput(attrs={'class': 'form-control'}),
        }


class ContactForm(forms.ModelForm):
    """Formulaire pour les messages de contact"""
    
    class Meta:
        model = Contact
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }


class EventAttendanceAggregateForm(forms.ModelForm):
    """Formulaire pour les compteurs démographiques de présence"""
    
    class Meta:
        model = EventAttendanceAggregate
        fields = [
            'male_adults', 'female_adults',
            'young_men', 'young_women',
            'male_children', 'female_children',
            'elderly_men', 'elderly_women',
        ]
        widgets = {
            'male_adults': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'placeholder': '0'}),
            'female_adults': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'placeholder': '0'}),
            'young_men': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'placeholder': '0'}),
            'young_women': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'placeholder': '0'}),
            'male_children': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'placeholder': '0'}),
            'female_children': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'placeholder': '0'}),
            'elderly_men': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'placeholder': '0'}),
            'elderly_women': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'placeholder': '0'}),
        }
