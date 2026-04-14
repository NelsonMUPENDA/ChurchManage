# views.py - Vues Django traditionnelles pour le rendu côté serveur
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.db.models import Count, Q, Sum
from django.utils import timezone
from django.core.paginator import Paginator
from datetime import timedelta

from .models import (
    Member, Family, HomeGroup, Department, Ministry, Event, Attendance,
    EvangelismActivity, TrainingEvent, MarriageRecord,
    FinancialCategory, FinancialTransaction, Announcement, Document, LogisticsItem,
    ChurchBiography, Contact, ChurchSettings
)
from .forms import (
    MemberForm, FamilyForm, HomeGroupForm, DepartmentForm, MinistryForm,
    EventForm, AttendanceForm, EvangelismActivityForm, TrainingEventForm, MarriageRecordForm,
    FinancialCategoryForm, FinancialTransactionForm, AnnouncementForm, DocumentForm, LogisticsItemForm,
    LoginForm, UserCreateForm, UserUpdateForm, ProfileUpdateForm, PasswordChangeCustomForm
)
from .permissions import (
    role_required, admin_required, finance_required, pastor_required,
    member_management_required, can_access_menu, can_create, can_edit, can_delete
)

User = get_user_model()


# ============================================================
# Authentification
# ============================================================

def login_view(request):
    """Page de connexion avec authentification Django"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    # Récupérer les paramètres de l'église
    try:
        church_settings = ChurchSettings.objects.first()
    except:
        church_settings = None
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenue, {user.first_name or username}!')
                return redirect('dashboard')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form, 'church_settings': church_settings})


def logout_view(request):
    """Déconnexion"""
    logout(request)
    messages.success(request, 'Vous avez été déconnecté.')
    return redirect('home')


# ============================================================
# Pages publiques
# ============================================================

def index(request):
    """Page d'accueil publique"""
    context = {
        'upcoming_events': Event.objects.filter(
            date__gte=timezone.now().date(),
            is_published=True
        ).order_by('date', 'time')[:5],
    }
    return render(request, 'index.html', context)


def public_about(request):
    """Page À propos"""
    context = {
        'biography': ChurchBiography.objects.filter(is_active=True).first(),
    }
    return render(request, 'public-about.html', context)


def contact(request):
    """Page Contact"""
    if request.method == 'POST':
        from .forms import ContactForm
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre message a été envoyé avec succès!')
            return redirect('contact')
    else:
        from .forms import ContactForm
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})


def public_events(request):
    """Page publique des événements"""
    today = timezone.now().date()
    
    events = Event.objects.filter(
        is_published=True
    ).order_by('date', 'time')
    
    upcoming_events = events.filter(date__gte=today)
    past_events = events.filter(date__lt=today)
    
    event_type = request.GET.get('type', '')
    if event_type:
        upcoming_events = upcoming_events.filter(event_type=event_type)
        past_events = past_events.filter(event_type=event_type)
    
    return render(request, 'public-events.html', {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'event_type': event_type,
    })


# ============================================================
# Tableau de bord
# ============================================================

@login_required
def dashboard(request):
    """Tableau de bord admin avec statistiques complètes"""
    user = request.user
    
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_start = today.replace(day=1)
    
    # Statistiques membres
    total_members = Member.objects.count()
    new_members_week = Member.objects.filter(created_at__date__gte=week_ago).count()
    new_members_month = Member.objects.filter(created_at__date__gte=month_start).count()
    
    # Statistiques événements
    upcoming_events = Event.objects.filter(date__gte=today, is_published=True).count()
    events_this_week = Event.objects.filter(date__gte=week_ago, date__lte=today).count()
    events_this_month = Event.objects.filter(date__month=today.month, date__year=today.year).count()
    
    # Événements à venir (liste)
    upcoming_events_list = Event.objects.filter(
        date__gte=today, is_published=True
    ).order_by('date', 'time')[:5]
    
    # Derniers événements passés
    recent_events = Event.objects.filter(
        date__lt=today
    ).order_by('-date')[:3]
    
    # Statistiques finances
    total_in_month = FinancialTransaction.objects.filter(
        direction='in', date__gte=month_start
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    total_out_month = FinancialTransaction.objects.filter(
        direction='out', date__gte=month_start
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # Statistiques présences
    attendance_week = Attendance.objects.filter(
        event__date__gte=week_ago, attended=True
    ).count()
    
    # Annonces actives
    active_announcements = Announcement.objects.filter(is_active=True).count()
    recent_announcements = Announcement.objects.filter(
        is_active=True
    ).order_by('-created_at')[:5]
    
    # Anniversaires du mois
    from django.db.models.functions import ExtractMonth, ExtractDay
    birthdays_this_month = Member.objects.annotate(
        birth_month=ExtractMonth('birth_date'),
        birth_day=ExtractDay('birth_date')
    ).filter(birth_month=today.month).order_by('birth_day')
    
    # Paramètres de l'église
    try:
        church_settings = ChurchSettings.objects.first()
    except:
        church_settings = None
    
    context = {
        'user': user,
        'today': today,
        # Membres
        'total_members': total_members,
        'new_members_week': new_members_week,
        'new_members_month': new_members_month,
        # Événements
        'upcoming_events': upcoming_events,
        'events_this_week': events_this_week,
        'events_this_month': events_this_month,
        'upcoming_events_list': upcoming_events_list,
        'recent_events': recent_events,
        # Finances
        'total_in_month': total_in_month,
        'total_out_month': total_out_month,
        'balance_month': total_in_month - total_out_month,
        # Présences
        'attendance_week': attendance_week,
        # Annonces
        'active_announcements': active_announcements,
        'recent_announcements': recent_announcements,
        # Anniversaires
        'birthdays_this_month': birthdays_this_month,
        # Paramètres de l'église
        'church_settings': church_settings,
    }
    return render(request, 'dashboard/dashboard.html', context)


# ============================================================
# Membres - CRUD
# ============================================================

@login_required
def member_list(request):
    """Liste des membres avec pagination, recherche et filtres"""
    members = Member.objects.select_related('user').all()
    
    # Recherche
    search = request.GET.get('q', '')
    if search:
        members = members.filter(
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search) |
            Q(user__email__icontains=search) |
            Q(member_number__icontains=search)
        )
    
    # Filtre par statut
    status_filter = request.GET.get('status', '')
    if status_filter == 'active':
        members = members.filter(is_active=True)
    elif status_filter == 'inactive':
        members = members.filter(is_active=False)
    elif status_filter == 'visitor':
        members = members.filter(user__isnull=True)
    
    # Statistiques
    from django.utils import timezone
    from datetime import timedelta
    
    total_members = Member.objects.count()
    active_members = Member.objects.filter(is_active=True).count()
    new_members = Member.objects.filter(
        created_at__gte=timezone.now() - timedelta(days=30)
    ).count()
    married_members = Member.objects.filter(marital_status='married').count()
    
    # Pagination
    paginator = Paginator(members, 20)  # 20 membres par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'dashboard/members.html', {
        'members': page_obj,
        'search': search,
        'status_filter': status_filter,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'total_members': total_members,
        'active_members': active_members,
        'new_members': new_members,
        'married_members': married_members,
    })


@login_required
def member_detail(request, pk):
    """Détail d'un membre"""
    member = get_object_or_404(Member, pk=pk)
    attendance_history = Attendance.objects.filter(
        member=member
    ).order_by('-event__date')[:10]
    
    return render(request, 'dashboard/member-detail.html', {
        'member': member,
        'attendance_history': attendance_history
    })


@login_required
@member_management_required
def member_create(request):
    """Créer un nouveau membre"""
    if not can_create(request.user):
        messages.error(request, "Vous n'avez pas la permission de créer des membres.")
        return redirect('member-list')
    
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES)
        if form.is_valid():
            member = form.save()
            messages.success(request, f'Membre {member.user.first_name} {member.user.last_name} créé avec succès!')
            return redirect('member-list')
    else:
        form = MemberForm()
    
    return render(request, 'dashboard/member-form.html', {
        'form': form,
        'title': 'Ajouter un Membre',
        'action': 'Créer'
    })


@login_required
@member_management_required
def member_edit(request, pk):
    """Modifier un membre"""
    if not can_edit(request.user):
        messages.error(request, "Vous n'avez pas la permission de modifier des membres.")
        return redirect('member-detail', pk=pk)
    
    member = get_object_or_404(Member, pk=pk)
    
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, f'Membre {member.user.first_name} {member.user.last_name} modifié avec succès!')
            return redirect('member-list')
    else:
        form = MemberForm(instance=member)
    
    return render(request, 'dashboard/member-form.html', {
        'form': form,
        'member': member,
        'title': 'Modifier le Membre',
        'action': 'Modifier'
    })


@login_required
@member_management_required
def member_delete(request, pk):
    """Supprimer un membre"""
    if not can_delete(request.user):
        messages.error(request, "Vous n'avez pas la permission de supprimer des membres.")
        return redirect('member-detail', pk=pk)
    
    member = get_object_or_404(Member, pk=pk)
    
    if request.method == 'POST':
        member.delete()
        messages.success(request, 'Membre supprimé avec succès!')
        return redirect('member-list')
    
    return render(request, 'dashboard/members.html', {'member': member, 'delete_confirm': True})


@login_required
def member_print_list(request):
    """Imprimer la liste des membres (PDF)"""
    from django.http import HttpResponse
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import cm
    from io import BytesIO
    
    members = Member.objects.select_related('user').filter(is_active=True)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="liste_membres.pdf"'
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    
    styles = getSampleStyleSheet()
    elements.append(Paragraph("Liste des Membres", styles['Heading1']))
    elements.append(Spacer(1, 0.5*cm))
    
    data = [['N°', 'Nom', 'Prénom', 'Téléphone', 'Email']]
    for idx, member in enumerate(members, 1):
        data.append([
            str(idx),
            member.user.last_name if member.user else '',
            member.user.first_name if member.user else '',
            member.user.phone if member.user else '',
            member.user.email if member.user else ''
        ])
    
    table = Table(data, colWidths=[1*cm, 4*cm, 4*cm, 3*cm, 5*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(table)
    doc.build(elements)
    
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


@login_required
def member_export(request):
    """Exporter les membres en CSV"""
    import csv
    from django.http import HttpResponse
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="membres.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['N° Membre', 'Nom', 'Prénom', 'Email', 'Téléphone', 'Genre', 'Statut'])
    
    members = Member.objects.select_related('user').all()
    for member in members:
        writer.writerow([
            member.member_number,
            member.user.last_name if member.user else '',
            member.user.first_name if member.user else '',
            member.user.email if member.user else '',
            member.user.phone if member.user else '',
            member.get_gender_display() if member.gender else '',
            'Actif' if member.is_active else 'Inactif'
        ])
    
    return response


@login_required
def member_print_card(request, pk):
    """Imprimer la carte de membre (PDF) avec QR code"""
    from django.http import HttpResponse
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, Image
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.lib.enums import TA_CENTER
    from io import BytesIO
    
    member = get_object_or_404(Member, pk=pk)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="carte_membre_{member.member_number}.pdf"'
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    
    styles = getSampleStyleSheet()
    
    # En-tête église
    elements.append(Paragraph("ÉGLISE CONSOLATION ET PAIX DIVINE", styles['Heading2']))
    elements.append(Paragraph("Carte de Membre", styles['Heading3']))
    elements.append(Spacer(1, 0.5*cm))
    
    # Numéro de membre en grand
    id_style = ParagraphStyle(
        'IDStyle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#6366f1'),
        alignment=TA_CENTER
    )
    elements.append(Paragraph(member.member_number, id_style))
    elements.append(Spacer(1, 0.5*cm))
    
    # Informations du membre
    data = [
        ['NOM:', member.user.last_name.upper() if member.user else ''],
        ['PRÉNOM:', member.user.first_name if member.user else ''],
        ['TÉLÉPHONE:', member.user.phone if member.user else ''],
        ['DATE DE NAISSANCE:', str(member.birth_date) if member.birth_date else ''],
        ['GENRE:', member.get_gender_display() if member.gender else ''],
        ['POSITION:', member.church_position or 'Membre'],
    ]
    
    table = Table(data, colWidths=[5*cm, 9*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f1f5f9')),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#475569')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 1*cm))
    
    # QR Code
    if member.qr_code and member.qr_code.path:
        try:
            elements.append(Paragraph("Scannez pour vérifier l'authenticité:", styles['Normal']))
            elements.append(Spacer(1, 0.3*cm))
            img = Image(member.qr_code.path, width=4*cm, height=4*cm)
            elements.append(img)
        except:
            pass
    
    elements.append(Spacer(1, 0.5*cm))
    elements.append(Paragraph("Cette carte est strictement personnelle.", styles['Normal']))
    elements.append(Paragraph("En cas de perte, veuillez contacter l'administration.", styles['Normal']))
    
    doc.build(elements)
    
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


# ============================================================
# Familles - CRUD
# ============================================================

@login_required
def family_list(request):
    """Liste des familles"""
    families = Family.objects.all().prefetch_related('members')
    return render(request, 'dashboard/members.html', {'families': families, 'view': 'families'})


@login_required
def family_create(request):
    """Créer une famille"""
    if request.method == 'POST':
        form = FamilyForm(request.POST)
        if form.is_valid():
            family = form.save()
            messages.success(request, f'Famille {family.name} créée avec succès!')
            return redirect('family-list')
    else:
        form = FamilyForm()
    
    return render(request, 'dashboard/members.html', {'form': form, 'action': 'Créer', 'view': 'family_form'})


@login_required
def family_edit(request, pk):
    """Modifier une famille"""
    family = get_object_or_404(Family, pk=pk)
    
    if request.method == 'POST':
        form = FamilyForm(request.POST, instance=family)
        if form.is_valid():
            form.save()
            messages.success(request, f'Famille {family.name} modifiée avec succès!')
            return redirect('family-list')
    else:
        form = FamilyForm(instance=family)
    
    return render(request, 'dashboard/members.html', {
        'form': form,
        'family': family,
        'action': 'Modifier',
        'view': 'family_form'
    })


@login_required
def family_delete(request, pk):
    """Supprimer une famille"""
    family = get_object_or_404(Family, pk=pk)
    
    if request.method == 'POST':
        family.delete()
        messages.success(request, 'Famille supprimée avec succès!')
        return redirect('family-list')
    
    return render(request, 'dashboard/members.html', {'family': family, 'delete_confirm': True, 'view': 'families'})


# ============================================================
# Groupes de maison - CRUD
# ============================================================

@login_required
def homegroup_list(request):
    """Liste des groupes de maison"""
    homegroups = HomeGroup.objects.all().select_related('leader')
    return render(request, 'dashboard/members.html', {'homegroups': homegroups, 'view': 'homegroups'})


@login_required
def homegroup_create(request):
    """Créer un groupe de maison"""
    if request.method == 'POST':
        form = HomeGroupForm(request.POST)
        if form.is_valid():
            homegroup = form.save()
            messages.success(request, f'Groupe de maison {homegroup.name} créé avec succès!')
            return redirect('homegroup-list')
    else:
        form = HomeGroupForm()
    
    return render(request, 'dashboard/members.html', {'form': form, 'action': 'Créer', 'view': 'homegroup_form'})


@login_required
def homegroup_edit(request, pk):
    """Modifier un groupe de maison"""
    homegroup = get_object_or_404(HomeGroup, pk=pk)
    
    if request.method == 'POST':
        form = HomeGroupForm(request.POST, instance=homegroup)
        if form.is_valid():
            form.save()
            messages.success(request, f'Groupe de maison {homegroup.name} modifié avec succès!')
            return redirect('homegroup-list')
    else:
        form = HomeGroupForm(instance=homegroup)
    
    return render(request, 'dashboard/members.html', {
        'form': form,
        'homegroup': homegroup,
        'action': 'Modifier',
        'view': 'homegroup_form'
    })


@login_required
def homegroup_delete(request, pk):
    """Supprimer un groupe de maison"""
    homegroup = get_object_or_404(HomeGroup, pk=pk)
    
    if request.method == 'POST':
        homegroup.delete()
        messages.success(request, 'Groupe de maison supprimé avec succès!')
        return redirect('homegroup-list')
    
    return render(request, 'dashboard/members.html', {'homegroup': homegroup, 'delete_confirm': True, 'view': 'homegroups'})


# ============================================================
# Départements - CRUD
# ============================================================

@login_required
def department_list(request):
    """Liste des départements"""
    departments = Department.objects.all().select_related('head')
    return render(request, 'dashboard/members.html', {'departments': departments, 'view': 'departments'})


@login_required
def department_create(request):
    """Créer un département"""
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            department = form.save()
            messages.success(request, f'Département {department.name} créé avec succès!')
            return redirect('department-list')
    else:
        form = DepartmentForm()
    
    return render(request, 'dashboard/members.html', {'form': form, 'action': 'Créer', 'view': 'department_form'})


@login_required
def department_edit(request, pk):
    """Modifier un département"""
    department = get_object_or_404(Department, pk=pk)
    
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, f'Département {department.name} modifié avec succès!')
            return redirect('department-list')
    else:
        form = DepartmentForm(instance=department)
    
    return render(request, 'dashboard/members.html', {
        'form': form,
        'department': department,
        'action': 'Modifier',
        'view': 'department_form'
    })


@login_required
def department_delete(request, pk):
    """Supprimer un département"""
    department = get_object_or_404(Department, pk=pk)
    
    if request.method == 'POST':
        department.delete()
        messages.success(request, 'Département supprimé avec succès!')
        return redirect('department-list')
    
    return render(request, 'dashboard/members.html', {'department': department, 'delete_confirm': True, 'view': 'departments'})


# ============================================================
# Ministères - CRUD
# ============================================================

@login_required
def ministry_list(request):
    """Liste des ministères"""
    ministries = Ministry.objects.all().select_related('leader')
    return render(request, 'dashboard/members.html', {'ministries': ministries, 'view': 'ministries'})


@login_required
def ministry_create(request):
    """Créer un ministère"""
    if request.method == 'POST':
        form = MinistryForm(request.POST)
        if form.is_valid():
            ministry = form.save()
            messages.success(request, f'Ministère {ministry.name} créé avec succès!')
            return redirect('ministry-list')
    else:
        form = MinistryForm()
    
    return render(request, 'dashboard/members.html', {'form': form, 'action': 'Créer', 'view': 'ministry_form'})


@login_required
def ministry_edit(request, pk):
    """Modifier un ministère"""
    ministry = get_object_or_404(Ministry, pk=pk)
    
    if request.method == 'POST':
        form = MinistryForm(request.POST, instance=ministry)
        if form.is_valid():
            form.save()
            messages.success(request, f'Ministère {ministry.name} modifié avec succès!')
            return redirect('ministry-list')
    else:
        form = MinistryForm(instance=ministry)
    
    return render(request, 'dashboard/members.html', {
        'form': form,
        'ministry': ministry,
        'action': 'Modifier',
        'view': 'ministry_form'
    })


@login_required
def ministry_delete(request, pk):
    """Supprimer un ministère"""
    ministry = get_object_or_404(Ministry, pk=pk)
    
    if request.method == 'POST':
        ministry.delete()
        messages.success(request, 'Ministère supprimé avec succès!')
        return redirect('ministry-list')
    
    return render(request, 'dashboard/members.html', {'ministry': ministry, 'delete_confirm': True, 'view': 'ministries'})


# ============================================================
# Événements - CRUD
# ============================================================

@login_required
def event_list(request):
    """Liste des événements avec pagination, recherche et filtres"""
    from datetime import date, timedelta
    
    events = Event.objects.all().order_by('-date', '-time')
    
    # Recherche
    search = request.GET.get('q', '')
    if search:
        events = events.filter(title__icontains=search)
    
    # Filtre par type
    event_type = request.GET.get('type', '')
    if event_type:
        events = events.filter(event_type=event_type)
    
    # Filtre par statut
    status_filter = request.GET.get('status', '')
    today = date.today()
    if status_filter == 'upcoming':
        events = events.filter(date__gte=today)
    elif status_filter == 'past':
        events = events.filter(date__lt=today)
    elif status_filter == 'published':
        events = events.filter(is_published=True)
    
    # Statistiques
    total_events = Event.objects.count()
    upcoming_events = Event.objects.filter(date__gte=today).count()
    this_week_start = today - timedelta(days=today.weekday())
    this_week_end = this_week_start + timedelta(days=6)
    this_week_events = Event.objects.filter(date__range=[this_week_start, this_week_end]).count()
    published_events = Event.objects.filter(is_published=True).count()
    
    # Pagination
    paginator = Paginator(events, 12)  # 12 événements par page (grid layout)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'dashboard/events.html', {
        'events': page_obj,
        'event_type': event_type,
        'status_filter': status_filter,
        'search': search,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'event_types': Event.EVENT_TYPE_CHOICES,
        'total_events': total_events,
        'upcoming_events': upcoming_events,
        'this_week_events': this_week_events,
        'published_events': published_events,
    })


@login_required
def event_detail(request, pk):
    """Détail d'un événement"""
    event = get_object_or_404(Event, pk=pk)
    attendance_list = Attendance.objects.filter(event=event).select_related('member')
    
    return render(request, 'dashboard/event-detail.html', {
        'event': event,
        'attendance_list': attendance_list,
        'total_attendance': attendance_list.count(),
        'present_count': attendance_list.filter(attended=True).count()
    })


@login_required
def event_create(request):
    """Créer un événement"""
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save()
            messages.success(request, f'Événement "{event.title}" créé avec succès!')
            return redirect('event-detail', pk=event.pk)
        else:
            # Form has errors - return with error messages
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = EventForm()

    departments = Department.objects.all()
    return render(request, 'dashboard/events.html', {
        'form': form, 
        'action': 'Créer', 
        'view': 'event_form',
        'departments': departments
    })


@login_required
def event_edit(request, pk):
    """Modifier un événement"""
    event = get_object_or_404(Event, pk=pk)
    
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, f'Événement "{event.title}" modifié avec succès!')
            return redirect('event-detail', pk=event.pk)
    else:
        form = EventForm(instance=event)
    
    departments = Department.objects.all()
    return render(request, 'dashboard/events.html', {
        'form': form,
        'event': event,
        'action': 'Modifier',
        'view': 'event_form',
        'departments': departments
    })


@login_required
def event_delete(request, pk):
    """Supprimer un événement"""
    event = get_object_or_404(Event, pk=pk)
    
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Événement supprimé avec succès!')
        return redirect('event-list')
    
    return render(request, 'dashboard/events.html', {'event': event, 'delete_confirm': True})


# ============================================================
# Présences (Pointage)
# ============================================================

@login_required
def attendance_list(request):
    """Liste des présences"""
    attendances = Attendance.objects.all().select_related('event', 'member').order_by('-event__date')
    return render(request, 'dashboard/diaconat.html', {'attendances': attendances, 'view': 'attendance_list'})


@login_required
def attendance_event(request, event_pk):
    """Pointage pour un événement spécifique"""
    event = get_object_or_404(Event, pk=event_pk)

    if request.method == 'POST':
        action = request.POST.get('action', '')
        member_id = request.POST.get('member_id')

        if action == 'mark_all_present':
            # Mark all active members as present
            members = Member.objects.filter(status='active')
            for member in members:
                attendance, created = Attendance.objects.get_or_create(
                    event=event,
                    member=member,
                    defaults={'attended': True, 'checked_in_at': timezone.now()}
                )
                if not created:
                    attendance.attended = True
                    attendance.checked_in_at = timezone.now()
                    attendance.save()
            messages.success(request, f'Tous les membres ont été marqués présents!')
            return redirect('attendance-event', event_pk=event_pk)

        elif action == 'reset':
            # Reset all attendances for this event
            Attendance.objects.filter(event=event).delete()
            messages.success(request, 'Pointage réinitialisé!')
            return redirect('attendance-event', event_pk=event_pk)

        elif member_id and action in ['present', 'absent']:
            # Mark specific member
            member = get_object_or_404(Member, pk=member_id)
            attended = action == 'present'
            attendance, created = Attendance.objects.get_or_create(
                event=event,
                member=member,
                defaults={'attended': attended, 'checked_in_at': timezone.now() if attended else None}
            )
            if not created:
                attendance.attended = attended
                attendance.checked_in_at = timezone.now() if attended else None
                attendance.save()
            messages.success(request, f'Présence enregistrée pour {member.get_full_name}!')
            return redirect('attendance-event', event_pk=event_pk)

        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Présence enregistrée avec succès!')
            return redirect('attendance-event', event_pk=event_pk)
    else:
        form = AttendanceForm(initial={'event': event})

    # Get all active members
    members = Member.objects.filter(status='active').order_by('last_name', 'first_name')

    # Get existing attendances for this event
    attendances = Attendance.objects.filter(event=event).select_related('member')
    member_attendance = {a.member_id: a for a in attendances}

    # Calculate stats
    present_count = attendances.filter(attended=True).count()
    absent_count = attendances.filter(attended=False).count()
    total_members = members.count()
    not_marked_count = total_members - present_count - absent_count

    # Calculate attendance rate for progress ring
    attendance_rate = round((present_count / total_members * 100)) if total_members > 0 else 0
    attendance_offset = 326.73 - (attendance_rate / 100 * 326.73)  # 326.73 is circumference of circle r=52

    return render(request, 'dashboard/attendance.html', {
        'event': event,
        'form': form,
        'members': members,
        'member_attendance': member_attendance,
        'present_count': present_count,
        'absent_count': absent_count,
        'not_marked_count': not_marked_count,
        'total_members': total_members,
        'attendance_rate': attendance_rate,
        'attendance_offset': attendance_offset,
    })


# ============================================================
# Finances - CRUD
# ============================================================

@login_required
@finance_required
def finance_list(request):
    """Liste des transactions financières"""
    transactions = FinancialTransaction.objects.all().select_related('category', 'member').order_by('-date', '-created_at')
    
    context = {
        'transactions': transactions[:100],
        'total_in': FinancialTransaction.objects.filter(direction='in').aggregate(total=Sum('amount'))['total'] or 0,
        'total_out': FinancialTransaction.objects.filter(direction='out').aggregate(total=Sum('amount'))['total'] or 0,
    }
    return render(request, 'finances.html', context)


@login_required
@finance_required
def transaction_create(request):
    """Créer une transaction"""
    if request.method == 'POST':
        form = FinancialTransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save()
            messages.success(request, f'Transaction {transaction.description} enregistrée avec succès!')
            return redirect('finance-list')
    else:
        form = FinancialTransactionForm()
    
    return render(request, 'dashboard/finances.html', {'form': form, 'action': 'Créer', 'view': 'transaction_form'})


@login_required
@finance_required
def transaction_edit(request, pk):
    """Modifier une transaction"""
    transaction = get_object_or_404(FinancialTransaction, pk=pk)
    
    if request.method == 'POST':
        form = FinancialTransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transaction modifiée avec succès!')
            return redirect('finance-list')
    else:
        form = FinancialTransactionForm(instance=transaction)
    
    return render(request, 'dashboard/finances.html', {
        'form': form,
        'transaction': transaction,
        'action': 'Modifier',
        'view': 'transaction_form'
    })


@login_required
@finance_required
def transaction_delete(request, pk):
    """Supprimer une transaction"""
    transaction = get_object_or_404(FinancialTransaction, pk=pk)
    
    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'Transaction supprimée avec succès!')
        return redirect('finance-list')
    
    return render(request, 'dashboard/finances.html', {'transaction': transaction, 'delete_confirm': True})


@login_required
@finance_required
def category_list(request):
    """Liste des catégories financières"""
    categories = FinancialCategory.objects.all()
    return render(request, 'dashboard/finances.html', {'categories': categories, 'view': 'category_list'})


@login_required
@finance_required
def category_create(request):
    """Créer une catégorie"""
    if request.method == 'POST':
        form = FinancialCategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Catégorie {category.name} créée avec succès!')
            return redirect('category-list')
    else:
        form = FinancialCategoryForm()
    
    return render(request, 'dashboard/finances.html', {'form': form, 'action': 'Créer', 'view': 'category_form'})


@login_required
@finance_required
def category_edit(request, pk):
    """Modifier une catégorie"""
    category = get_object_or_404(FinancialCategory, pk=pk)
    
    if request.method == 'POST':
        form = FinancialCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f'Catégorie {category.name} modifiée avec succès!')
            return redirect('category-list')
    else:
        form = FinancialCategoryForm(instance=category)
    
    return render(request, 'dashboard/finances.html', {
        'form': form,
        'category': category,
        'action': 'Modifier',
        'view': 'category_form'
    })


@login_required
def category_delete(request, pk):
    """Supprimer une catégorie"""
    category = get_object_or_404(FinancialCategory, pk=pk)
    
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Catégorie supprimée avec succès!')
        return redirect('category-list')
    
    return render(request, 'dashboard/finances.html', {'category': category, 'delete_confirm': True, 'view': 'category_list'})


# ============================================================
# Rapports
# ============================================================

@login_required
def reports(request):
    """Rapports et statistiques"""
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    context = {
        'stats': {
            'members': Member.objects.count(),
            'members_new_week': Member.objects.filter(created_at__date__gte=week_ago).count(),
            'members_new_month': Member.objects.filter(created_at__date__gte=month_ago).count(),
            'events_week': Event.objects.filter(date__range=[week_ago, today]).count(),
            'events_month': Event.objects.filter(date__range=[month_ago, today]).count(),
            'total_in': FinancialTransaction.objects.filter(direction='in').aggregate(total=Sum('amount'))['total'] or 0,
            'total_out': FinancialTransaction.objects.filter(direction='out').aggregate(total=Sum('amount'))['total'] or 0,
        }
    }
    return render(request, 'dashboard/reports.html', context)


# ============================================================
# Annonces - CRUD
# ============================================================

@login_required
def announcement_list(request):
    """Liste des annonces"""
    announcements = Announcement.objects.all().order_by('-created_at')
    return render(request, 'dashboard/announcements.html', {
        'announcements': announcements,
        'published_count': announcements.filter(is_active=True).count()
    })


@login_required
def announcement_detail(request, pk):
    """Détail d'une annonce"""
    announcement = get_object_or_404(Announcement, pk=pk)
    return render(request, 'dashboard/announcements.html', {'announcement': announcement, 'view': 'detail'})


@login_required
def announcement_create(request):
    """Créer une annonce"""
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request.FILES)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.created_by = request.user
            announcement.save()
            messages.success(request, f'Annonce {announcement.title} créée avec succès!')
            return redirect('announcement-list')
    else:
        form = AnnouncementForm()
    
    return render(request, 'dashboard/announcements.html', {'form': form, 'action': 'Créer', 'view': 'form'})


@login_required
def announcement_edit(request, pk):
    """Modifier une annonce"""
    announcement = get_object_or_404(Announcement, pk=pk)
    
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request.FILES, instance=announcement)
        if form.is_valid():
            form.save()
            messages.success(request, f'Annonce {announcement.title} modifiée avec succès!')
            return redirect('announcement-list')
    else:
        form = AnnouncementForm(instance=announcement)
    
    return render(request, 'dashboard/announcements.html', {
        'form': form,
        'announcement': announcement,
        'action': 'Modifier',
        'view': 'form'
    })


@login_required
def announcement_delete(request, pk):
    """Supprimer une annonce"""
    announcement = get_object_or_404(Announcement, pk=pk)
    
    if request.method == 'POST':
        announcement.delete()
        messages.success(request, 'Annonce supprimée avec succès!')
        return redirect('announcement-list')
    
    return render(request, 'dashboard/announcements.html', {'announcement': announcement, 'delete_confirm': True})


# ============================================================
# Diaconat (Pointage et Logistique)
# ============================================================

@login_required
def diaconat(request):
    """Diaconat - Pointage et logistique"""
    today = timezone.now().date()
    upcoming_events = Event.objects.filter(date__gte=today).order_by('date')[:10]
    
    context = {
        'events': upcoming_events,
        'logistics_items': LogisticsItem.objects.all()[:20]
    }
    return render(request, 'dashboard/diaconat.html', context)


@login_required
def diaconat_attendance(request):
    """Pointage pour le diaconat"""
    today = timezone.now().date()
    events = Event.objects.filter(date=today).order_by('time')
    return render(request, 'dashboard/diaconat.html', {'events': events, 'view': 'diaconat_attendance'})


# ============================================================
# Logistique - CRUD
# ============================================================

@login_required
def logistics_list(request):
    """Liste des éléments logistiques"""
    items = LogisticsItem.objects.all().select_related('responsible')
    return render(request, 'dashboard/diaconat.html', {'items': items, 'view': 'logistics_list'})


@login_required
def logistics_create(request):
    """Créer un élément logistique"""
    if request.method == 'POST':
        form = LogisticsItemForm(request.POST)
        if form.is_valid():
            item = form.save()
            messages.success(request, f'Élément {item.name} créé avec succès!')
            return redirect('logistics-list')
    else:
        form = LogisticsItemForm()
    
    return render(request, 'dashboard/diaconat.html', {'form': form, 'action': 'Créer', 'view': 'logistics_form'})


@login_required
def logistics_edit(request, pk):
    """Modifier un élément logistique"""
    item = get_object_or_404(LogisticsItem, pk=pk)
    
    if request.method == 'POST':
        form = LogisticsItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f'Élément {item.name} modifié avec succès!')
            return redirect('logistics-list')
    else:
        form = LogisticsItemForm(instance=item)
    
    return render(request, 'dashboard/diaconat.html', {
        'form': form,
        'item': item,
        'action': 'Modifier',
        'view': 'logistics_form'
    })


@login_required
def logistics_delete(request, pk):
    """Supprimer un élément logistique"""
    item = get_object_or_404(LogisticsItem, pk=pk)
    
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Élément supprimé avec succès!')
        return redirect('logistics-list')
    
    return render(request, 'dashboard/diaconat.html', {'item': item, 'delete_confirm': True, 'view': 'logistics_list'})


# ============================================================
# Évangélisation - CRUD
# ============================================================

@login_required
def evangelisation_list(request):
    """Liste des activités d'évangélisation"""
    activities = EvangelismActivity.objects.all().order_by('-date', '-time')
    return render(request, 'dashboard/evangelisation.html', {'activities': activities})


@login_required
def evangelisation_create(request):
    """Créer une activité d'évangélisation"""
    if request.method == 'POST':
        form = EvangelismActivityForm(request.POST)
        if form.is_valid():
            activity = form.save()
            messages.success(request, f'Activité {activity.title} créée avec succès!')
            return redirect('evangelisation-list')
    else:
        form = EvangelismActivityForm()
    
    return render(request, 'dashboard/evangelisation.html', {'form': form, 'action': 'Créer', 'view': 'form'})


@login_required
def evangelisation_edit(request, pk):
    """Modifier une activité d'évangélisation"""
    activity = get_object_or_404(EvangelismActivity, pk=pk)
    
    if request.method == 'POST':
        form = EvangelismActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            messages.success(request, f'Activité {activity.title} modifiée avec succès!')
            return redirect('evangelisation-list')
    else:
        form = EvangelismActivityForm(instance=activity)
    
    return render(request, 'dashboard/evangelisation.html', {
        'form': form,
        'activity': activity,
        'action': 'Modifier',
        'view': 'form'
    })


@login_required
def evangelisation_delete(request, pk):
    """Supprimer une activité d'évangélisation"""
    activity = get_object_or_404(EvangelismActivity, pk=pk)
    
    if request.method == 'POST':
        activity.delete()
        messages.success(request, 'Activité supprimée avec succès!')
        return redirect('evangelisation-list')
    
    return render(request, 'dashboard/evangelisation.html', {'activity': activity, 'delete_confirm': True})


# ============================================================
# Formations - CRUD
# ============================================================

@login_required
def training_list(request):
    """Liste des formations"""
    trainings = TrainingEvent.objects.all().order_by('-date', '-time')
    return render(request, 'dashboard/evangelisation.html', {'trainings': trainings, 'view': 'trainings'})


@login_required
def training_create(request):
    """Créer une formation"""
    if request.method == 'POST':
        form = TrainingEventForm(request.POST)
        if form.is_valid():
            training = form.save()
            messages.success(request, f'Formation {training.title} créée avec succès!')
            return redirect('training-list')
    else:
        form = TrainingEventForm()
    
    return render(request, 'dashboard/evangelisation.html', {'form': form, 'action': 'Créer', 'view': 'training_form'})


@login_required
def training_edit(request, pk):
    """Modifier une formation"""
    training = get_object_or_404(TrainingEvent, pk=pk)
    
    if request.method == 'POST':
        form = TrainingEventForm(request.POST, instance=training)
        if form.is_valid():
            form.save()
            messages.success(request, f'Formation {training.title} modifiée avec succès!')
            return redirect('training-list')
    else:
        form = TrainingEventForm(instance=training)
    
    return render(request, 'dashboard/evangelisation.html', {
        'form': form,
        'training': training,
        'action': 'Modifier',
        'view': 'training_form'
    })


@login_required
def training_delete(request, pk):
    """Supprimer une formation"""
    training = get_object_or_404(TrainingEvent, pk=pk)
    
    if request.method == 'POST':
        training.delete()
        messages.success(request, 'Formation supprimée avec succès!')
        return redirect('training-list')
    
    return render(request, 'dashboard/evangelisation.html', {'training': training, 'delete_confirm': True, 'view': 'trainings'})


# ============================================================
# Mariages - CRUD
# ============================================================

@login_required
def marriage_list(request):
    """Liste des registres de mariage"""
    marriages = MarriageRecord.objects.all().select_related('groom', 'bride').order_by('-planned_date')
    return render(request, 'dashboard/mariage.html', {'marriages': marriages})


@login_required
def marriage_detail(request, pk):
    """Détail d'un registre de mariage"""
    marriage = get_object_or_404(MarriageRecord, pk=pk)
    return render(request, 'dashboard/mariage.html', {'marriage': marriage, 'view': 'detail'})


@login_required
def marriage_create(request):
    """Créer un registre de mariage"""
    if request.method == 'POST':
        form = MarriageRecordForm(request.POST)
        if form.is_valid():
            marriage = form.save()
            messages.success(request, 'Registre de mariage créé avec succès!')
            return redirect('marriage-detail', pk=marriage.pk)
    else:
        form = MarriageRecordForm()
    
    return render(request, 'dashboard/mariage.html', {'form': form, 'action': 'Créer', 'view': 'form'})


@login_required
def marriage_edit(request, pk):
    """Modifier un registre de mariage"""
    marriage = get_object_or_404(MarriageRecord, pk=pk)
    
    if request.method == 'POST':
        form = MarriageRecordForm(request.POST, instance=marriage)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registre de mariage modifié avec succès!')
            return redirect('marriage-detail', pk=marriage.pk)
    else:
        form = MarriageRecordForm(instance=marriage)
    
    return render(request, 'dashboard/mariage.html', {
        'form': form,
        'marriage': marriage,
        'action': 'Modifier',
        'view': 'form'
    })


@login_required
def marriage_delete(request, pk):
    """Supprimer un registre de mariage"""
    marriage = get_object_or_404(MarriageRecord, pk=pk)
    
    if request.method == 'POST':
        marriage.delete()
        messages.success(request, 'Registre de mariage supprimé avec succès!')
        return redirect('marriage-list')
    
    return render(request, 'dashboard/mariage.html', {'marriage': marriage, 'delete_confirm': True})


# ============================================================
# Documents - CRUD
# ============================================================

@login_required
def document_list(request):
    """Liste des documents"""
    documents = Document.objects.all().order_by('-uploaded_at')
    return render(request, 'dashboard/account.html', {'documents': documents, 'view': 'documents'})


@login_required
def document_create(request):
    """Uploader un document"""
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.uploaded_by = request.user
            document.save()
            messages.success(request, f'Document {document.title} uploadé avec succès!')
            return redirect('document-list')
    else:
        form = DocumentForm()
    
    return render(request, 'dashboard/account.html', {'form': form, 'action': 'Uploader', 'view': 'document_form'})


@login_required
def document_delete(request, pk):
    """Supprimer un document"""
    document = get_object_or_404(Document, pk=pk)
    
    if request.method == 'POST':
        document.delete()
        messages.success(request, 'Document supprimé avec succès!')
        return redirect('document-list')
    
    return render(request, 'dashboard/account.html', {'document': document, 'delete_confirm': True, 'view': 'documents'})


# ============================================================
# Compte utilisateur
# ============================================================

@login_required
def account(request):
    """Profil utilisateur complet"""
    user = request.user
    
    # Récupérer les informations du membre associé (si existe)
    try:
        member = Member.objects.select_related('user').get(user=user)
    except Member.DoesNotExist:
        member = None
    
    # Préparer les infos du membre pour l'affichage
    member_info = {}
    if member:
        member_info = {
            'Numéro de membre': member.member_number,
            'Date de naissance': member.birth_date.strftime('%d/%m/%Y') if member.birth_date else None,
            'Lieu de naissance': member.place_of_birth,
            'Genre': member.get_gender_display(),
            'Nationalité': member.nationality,
            'État civil': member.get_marital_status_display(),
            'Profession': member.occupation,
            'Fonction à l\'église': member.church_position,
            'Département': member.department.name if member.department else None,
            'Ministère': member.ministry.name if member.ministry else None,
            'Groupe de maison': member.home_group.name if member.home_group else None,
            'Date de baptême': member.baptism_date.strftime('%d/%m/%Y') if member.baptism_date else None,
            'Statut': 'Actif' if member.is_active else 'Inactif',
        }
    
    # Formulaires - Utiliser ProfileUpdateForm (sans role) pour son propre profil
    profile_form = ProfileUpdateForm(instance=user)
    password_form = PasswordChangeCustomForm(user=user)
    
    context = {
        'user': user,
        'member': member,
        'member_info': member_info,
        'profile_form': profile_form,
        'password_form': password_form,
        'active_page': 'account',
    }
    return render(request, 'dashboard/account.html', context)


@login_required
def account_edit(request):
    """Modifier le profil utilisateur"""
    user = request.user
    
    if request.method == 'POST':
        # Déterminer quel formulaire a été soumis
        form_type = request.POST.get('form_type', 'profile')
        
        if form_type == 'profile':
            form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profil modifié avec succès!')
                return redirect('account')
            else:
                # Recharger la page avec les erreurs
                try:
                    member = Member.objects.select_related('user').get(user=user)
                except Member.DoesNotExist:
                    member = None
                
                # Préparer member_info aussi pour le cas d'erreur
                member_info = {}
                if member:
                    member_info = {
                        'Numéro de membre': member.member_number,
                        'Date de naissance': member.birth_date.strftime('%d/%m/%Y') if member.birth_date else None,
                        'Lieu de naissance': member.place_of_birth,
                        'Genre': member.get_gender_display(),
                        'Nationalité': member.nationality,
                        'État civil': member.get_marital_status_display(),
                        'Profession': member.occupation,
                        'Fonction à l\'église': member.church_position,
                        'Département': member.department.name if member.department else None,
                        'Ministère': member.ministry.name if member.ministry else None,
                        'Groupe de maison': member.home_group.name if member.home_group else None,
                        'Date de baptême': member.baptism_date.strftime('%d/%m/%Y') if member.baptism_date else None,
                        'Statut': 'Actif' if member.is_active else 'Inactif',
                    }
                
                context = {
                    'user': user,
                    'member': member,
                    'member_info': member_info,
                    'profile_form': form,
                    'password_form': PasswordChangeCustomForm(user=user),
                    'active_page': 'account',
                }
                return render(request, 'dashboard/account.html', context)

        elif form_type == 'password':
            password_form = PasswordChangeCustomForm(user=user, data=request.POST)
            if password_form.is_valid():
                password_form.save()
                messages.success(request, 'Mot de passe changé avec succès! Veuillez vous reconnecter.')
                return redirect('logout')
            else:
                # Recharger la page avec les erreurs
                try:
                    member = Member.objects.select_related('user').get(user=user)
                except Member.DoesNotExist:
                    member = None
                
                member_info = {}
                if member:
                    member_info = {
                        'Numéro de membre': member.member_number,
                        'Date de naissance': member.birth_date.strftime('%d/%m/%Y') if member.birth_date else None,
                        'Lieu de naissance': member.place_of_birth,
                        'Genre': member.get_gender_display(),
                        'Nationalité': member.nationality,
                        'État civil': member.get_marital_status_display(),
                        'Profession': member.occupation,
                        'Fonction à l\'église': member.church_position,
                        'Département': member.department.name if member.department else None,
                        'Ministère': member.ministry.name if member.ministry else None,
                        'Groupe de maison': member.home_group.name if member.home_group else None,
                        'Date de baptême': member.baptism_date.strftime('%d/%m/%Y') if member.baptism_date else None,
                        'Statut': 'Actif' if member.is_active else 'Inactif',
                    }
                
                context = {
                    'user': user,
                    'member': member,
                    'member_info': member_info,
                    'profile_form': ProfileUpdateForm(instance=user),
                    'password_form': password_form,
                    'active_page': 'account',
                }
                return render(request, 'dashboard/account.html', context)
    
    return redirect('account')
