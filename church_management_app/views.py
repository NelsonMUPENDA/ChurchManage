from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from .models import Member, Event, FinancialTransaction, Announcement, Attendance, ChurchBiography

User = get_user_model()


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
    return render(request, 'contact.html')


def dashboard(request):
    """Tableau de bord admin"""
    user = request.user
    
    # Stats based on user role
    context = {
        'total_members': Member.objects.count() if user.is_staff else None,
        'upcoming_events': Event.objects.filter(
            date__gte=timezone.now().date()
        ).count(),
        'recent_announcements': Announcement.objects.filter(
            is_active=True
        ).order_by('-created_at')[:5],
    }
    return render(request, 'dashboard.html', context)


def members(request):
    """Liste des membres"""
    members_list = Member.objects.select_related('user').all()
    
    # Search filter
    search = request.GET.get('q', '')
    if search:
        members_list = members_list.filter(
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search) |
            Q(user__email__icontains=search)
        )
    
    context = {
        'members': members_list,
        'total_members': members_list.count(),
    }
    return render(request, 'members.html', context)


def member_detail(request, pk):
    """Détail d'un membre"""
    member = get_object_or_404(Member, pk=pk)
    context = {
        'member': member,
        'attendance_history': Attendance.objects.filter(
            member=member
        ).order_by('-event__date')[:10],
    }
    return render(request, 'member-detail.html', context)


def events(request):
    """Liste des événements"""
    events_list = Event.objects.all().order_by('-date', '-time')
    
    # Filter by type
    event_type = request.GET.get('type', '')
    if event_type:
        events_list = events_list.filter(event_type=event_type)
    
    context = {
        'events': events_list,
        'upcoming_count': Event.objects.filter(
            date__gte=timezone.now().date()
        ).count(),
    }
    return render(request, 'events.html', context)


def event_detail(request, pk):
    """Détail d'un événement"""
    event = get_object_or_404(Event, pk=pk)
    context = {
        'event': event,
        'attendance': Attendance.objects.filter(event=event),
        'attendance_stats': {
            'total': Attendance.objects.filter(event=event).count(),
            'present': Attendance.objects.filter(event=event, attended=True).count(),
        }
    }
    return render(request, 'event-detail.html', context)


def finances(request):
    """Gestion financière"""
    transactions = FinancialTransaction.objects.all().order_by('-date', '-created_at')
    
    context = {
        'transactions': transactions[:50],
        'total_in': FinancialTransaction.objects.filter(
            direction='in'
        ).aggregate(total=models.Sum('amount'))['total'] or 0,
        'total_out': FinancialTransaction.objects.filter(
            direction='out'
        ).aggregate(total=models.Sum('amount'))['total'] or 0,
    }
    return render(request, 'finances.html', context)


def reports(request):
    """Rapports et statistiques"""
    from django.utils import timezone
    from datetime import timedelta
    
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    
    context = {
        'stats': {
            'members': Member.objects.count(),
            'members_new_week': Member.objects.filter(
                created_at__date__gte=week_ago
            ).count(),
            'events_week': Event.objects.filter(
                date__range=[week_ago, today]
            ).count(),
            'attendance_avg': 0,  # Calculated from Attendance model
        }
    }
    return render(request, 'reports.html', context)


def announcements(request):
    """Gestion des annonces"""
    announcements_list = Announcement.objects.all().order_by('-created_at')
    context = {
        'announcements': announcements_list,
        'published_count': announcements_list.filter(is_active=True).count(),
    }
    return render(request, 'announcements.html', context)


def diaconat(request):
    """Diaconat - Pointage et logistique"""
    context = {
        'events': Event.objects.filter(
            date__gte=timezone.now().date()
        ).order_by('date')[:10],
    }
    return render(request, 'diaconat.html', context)


def evangelisation(request):
    """Activités d'évangélisation"""
    from .models import EvangelismActivity
    
    activities = EvangelismActivity.objects.all().order_by('-date')
    context = {
        'activities': activities,
        'stats': {
            'total': activities.count(),
            'this_month': activities.filter(
                date__month=timezone.now().month
            ).count(),
        }
    }
    return render(request, 'evangelisation.html', context)


def mariage(request):
    """Registre des mariages"""
    from .models import MarriageRecord
    
    marriages = MarriageRecord.objects.all().order_by('-planned_date')
    context = {
        'marriages': marriages,
        'total': marriages.count(),
        'upcoming': marriages.filter(
            planned_date__gte=timezone.now().date()
        ).count(),
    }
    return render(request, 'mariage.html', context)


def account(request):
    """Profil utilisateur"""
    return render(request, 'account.html', {
        'user': request.user,
    })


def login_page(request):
    """Page de connexion"""
    return render(request, 'login.html')


# Import supplémentaire nécessaire
from django.utils import timezone
from django.db import models
