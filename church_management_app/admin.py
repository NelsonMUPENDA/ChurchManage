from django.contrib import admin
from django.utils.html import format_html
from .models import User, Member, Family, HomeGroup, Department, Ministry, ActivityDuration, Event, Attendance, FinancialCategory, FinancialTransaction, Announcement, AnnouncementDeck, AnnouncementDeckItem, Document, Notification, AuditLogEntry, ChurchBiography, ChurchConsistory, Contact, ChurchSettings
from .forms import ChurchBiographyForm, ChurchConsistoryForm

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role', 'phone', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['username', 'email', 'phone']

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['member_number', 'user', 'birth_date', 'gender', 'nationality', 'is_active', 'created_at']
    list_filter = ['gender', 'nationality', 'is_active', 'created_at']
    search_fields = ['member_number', 'user__username', 'user__email', 'user__phone']

@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'created_at']
    search_fields = ['name', 'phone']

@admin.register(HomeGroup)
class HomeGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'leader', 'meeting_day', 'meeting_time', 'created_at']
    list_filter = ['meeting_day', 'created_at']
    search_fields = ['name', 'leader__user__username']

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'head', 'created_at']
    search_fields = ['name', 'head__user__username']

@admin.register(Ministry)
class MinistryAdmin(admin.ModelAdmin):
    list_display = ['name', 'leader', 'created_at']
    search_fields = ['name', 'leader__user__username']


@admin.register(ActivityDuration)
class ActivityDurationAdmin(admin.ModelAdmin):
    list_display = ['code', 'label', 'sort_order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['code', 'label']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_type', 'date', 'time', 'location', 'responsible', 'created_at']
    list_filter = ['event_type', 'date', 'created_at']
    search_fields = ['title', 'location', 'responsible__user__username']

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['event', 'member', 'attended', 'checked_in_at', 'created_at']
    list_filter = ['attended', 'created_at']
    search_fields = ['event__title', 'member__user__username']

@admin.register(FinancialCategory)
class FinancialCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

@admin.register(FinancialTransaction)
class FinancialTransactionAdmin(admin.ModelAdmin):
    list_display = ['amount', 'transaction_type', 'category', 'member', 'date', 'created_at']
    list_filter = ['transaction_type', 'date', 'created_at']
    search_fields = ['category__name', 'member__user__username']

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'published_date', 'is_active', 'created_at']
    list_filter = ['is_active', 'published_date', 'created_at']
    search_fields = ['title', 'author__username']


@admin.register(AnnouncementDeck)
class AnnouncementDeckAdmin(admin.ModelAdmin):
    list_display = ['title', 'event', 'generated_at', 'created_by', 'created_at']
    list_filter = ['generated_at', 'created_at']
    search_fields = ['title', 'event__title', 'created_by__username']


@admin.register(AnnouncementDeckItem)
class AnnouncementDeckItemAdmin(admin.ModelAdmin):
    list_display = ['deck', 'order', 'created_at']
    list_filter = ['created_at']
    search_fields = ['deck__title', 'text']

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'document_type', 'uploaded_by', 'uploaded_at', 'created_at']
    list_filter = ['document_type', 'uploaded_at', 'created_at']
    search_fields = ['title', 'uploaded_by__username']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'recipient', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['title', 'recipient__username']


@admin.register(AuditLogEntry)
class AuditLogEntryAdmin(admin.ModelAdmin):
    list_display = ['action', 'model', 'object_id', 'object_repr', 'actor', 'ip_address', 'created_at']
    list_filter = ['action', 'model', 'created_at']
    search_fields = ['object_id', 'object_repr', 'actor__username', 'model']


@admin.register(ChurchBiography)
class ChurchBiographyAdmin(admin.ModelAdmin):
    """Admin pour la gestion complète de la biographie et des informations de contact de l'église"""
    form = ChurchBiographyForm
    list_display = ['title', 'is_active', 'preview_contact', 'has_social_links', 'created_at', 'updated_at', 'created_by']
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['title', 'content', 'address', 'email', 'phone']
    readonly_fields = ['created_at', 'updated_at', 'created_by']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('title', 'content', 'is_active'),
            'description': 'Titre et contenu principal de la biographie'
        }),
        ('Coordonnées de contact', {
            'fields': ('address', 'phone', 'email'),
            'description': 'Informations de contact affichées sur la page Contact',
            'classes': ('wide',)
        }),
        ('Réseaux sociaux', {
            'fields': ('facebook_url', 'youtube_url', 'instagram_url'),
            'description': 'Liens vers les réseaux sociaux de l\'église',
            'classes': ('collapse',)
        }),
        ('Horaires des cultes', {
            'fields': ('service_times',),
            'description': 'Format JSON: [{"day": "Dimanche", "time": "9h00 - 12h00", "name": "Culte Dominical"}]',
            'classes': ('wide',)
        }),
        ('Métadonnées', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['make_active', 'make_inactive', 'duplicate_record']
    
    def preview_contact(self, obj):
        """Affiche un aperçu des informations de contact"""
        return format_html(
            '<div style="font-size: 12px;">'
            '<strong>📍</strong> {}<br>'
            '<strong>📞</strong> {}<br>'
            '<strong>✉️</strong> {}'
            '</div>',
            obj.address[:50] + '...' if obj.address and len(obj.address) > 50 else (obj.address or '-'),
            obj.phone or '-',
            obj.email or '-'
        )
    preview_contact.short_description = 'Aperçu contact'
    
    def has_social_links(self, obj):
        """Indique si des liens sociaux sont configurés"""
        links = []
        if obj.facebook_url:
            links.append('FB')
        if obj.youtube_url:
            links.append('YT')
        if obj.instagram_url:
            links.append('IG')
        return format_html(
            '<span style="color: {};">{}</span>',
            '#22c55e' if links else '#ef4444',
            ', '.join(links) if links else 'Aucun'
        )
    has_social_links.short_description = 'Réseaux sociaux'
    has_social_links.boolean = False
    
    def make_active(self, request, queryset):
        """Action pour activer les biographies sélectionnées"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} biographie(s) activée(s).')
    make_active.short_description = '✅ Activer les biographies sélectionnées'
    
    def make_inactive(self, request, queryset):
        """Action pour désactiver les biographies sélectionnées"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} biographie(s) désactivée(s).')
    make_inactive.short_description = '❌ Désactiver les biographies sélectionnées'
    
    def duplicate_record(self, request, queryset):
        """Action pour dupliquer une biographie"""
        for obj in queryset:
            obj.pk = None
            obj.title = f'{obj.title} (Copie)'
            obj.is_active = False
            obj.save()
        self.message_user(request, f'{queryset.count()} biographie(s) dupliquée(s).')
    duplicate_record.short_description = '📋 Dupliquer la biographie'
    
    def save_model(self, request, obj, form, change):
        """Auto-assignation du created_by lors de la création"""
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    class Media:
        css = {
            'all': ('admin/css/custom.css',)
        }


@admin.register(ChurchConsistory)
class ChurchConsistoryAdmin(admin.ModelAdmin):
    """Admin pour la gestion des informations du consistoire"""
    list_display = ['title', 'is_active', 'preview_content', 'created_at', 'updated_at', 'created_by']
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['title', 'content']
    readonly_fields = ['created_at', 'updated_at', 'created_by']
    
    fieldsets = (
        ('Informations du consistoire', {
            'fields': ('title', 'content', 'is_active'),
            'description': 'Gestion des informations du consistoire de l\'église'
        }),
        ('Métadonnées', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['make_active', 'make_inactive', 'duplicate_record']
    
    def preview_content(self, obj):
        """Affiche un aperçu du contenu"""
        content = obj.content[:100] if obj.content else ''
        return format_html(
            '<span style="font-size: 12px; color: #666;">{}...</span>',
            content
        )
    preview_content.short_description = 'Aperçu'
    
    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} consistoire(s) activé(s).')
    make_active.short_description = '✅ Activer'
    
    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} consistoire(s) désactivé(s).')
    make_inactive.short_description = '❌ Désactiver'
    
    def duplicate_record(self, request, queryset):
        for obj in queryset:
            obj.pk = None
            obj.title = f'{obj.title} (Copie)'
            obj.is_active = False
            obj.save()
        self.message_user(request, f'{queryset.count()} consistoire(s) dupliqué(s).')
    duplicate_record.short_description = '📋 Dupliquer'
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Admin pour la gestion des messages de contact"""
    list_display = ['name', 'email', 'subject', 'status_badge', 'phone', 'created_at', 'is_recent']
    list_filter = ['status', 'subject', 'created_at']
    search_fields = ['name', 'email', 'phone', 'message', 'notes']
    readonly_fields = ['created_at', 'updated_at', 'ip_address', 'user_agent']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Informations de l\'expéditeur', {
            'fields': ('name', 'email', 'phone'),
            'description': 'Coordonnées de la personne ayant envoyé le message'
        }),
        ('Message', {
            'fields': ('subject', 'message'),
            'classes': ('wide',)
        }),
        ('Gestion et suivi', {
            'fields': ('status', 'notes', 'answered_by', 'answered_at'),
            'classes': ('wide',)
        }),
        ('Métadonnées techniques', {
            'fields': ('ip_address', 'user_agent', 'created_at', 'updated_at'),
            'classes': ('collapse',),
            'description': 'Informations techniques (IP, navigateur, dates)'
        }),
    )
    
    actions = ['mark_as_read', 'mark_in_progress', 'mark_as_answered', 'mark_as_archived', 'delete_selected_messages']
    
    def status_badge(self, obj):
        """Affiche le statut avec une couleur"""
        colors = {
            'new': '#ef4444',  # Rouge
            'read': '#3b82f6',  # Bleu
            'in_progress': '#f59e0b',  # Orange
            'answered': '#22c55e',  # Vert
            'archived': '#6b7280',  # Gris
        }
        color = colors.get(obj.status, '#6b7280')
        status_labels = dict(Contact.STATUS_CHOICES)
        return format_html(
            '<span style="background: {}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">{}</span>',
            color,
            status_labels.get(obj.status, obj.status)
        )
    status_badge.short_description = 'Statut'
    
    def is_recent(self, obj):
        """Indique si le message est récent (moins de 24h)"""
        from django.utils import timezone
        from datetime import timedelta
        
        if obj.created_at and (timezone.now() - obj.created_at) < timedelta(hours=24):
            return format_html('<span style="color: #ef4444; font-weight: bold;">🆕 Nouveau</span>')
        return format_html('<span style="color: #6b7280;">-</span>')
    is_recent.short_description = 'Récent'
    
    def mark_as_read(self, request, queryset):
        """Marquer comme lu"""
        updated = queryset.update(status='read')
        self.message_user(request, f'{updated} message(s) marqué(s) comme lu(s).')
    mark_as_read.short_description = '✅ Marquer comme lu'
    
    def mark_in_progress(self, request, queryset):
        """Marquer en cours"""
        updated = queryset.update(status='in_progress')
        self.message_user(request, f'{updated} message(s) marqué(s) en cours.')
    mark_in_progress.short_description = '🔄 Marquer en cours'
    
    def mark_as_answered(self, request, queryset):
        """Marquer comme répondu"""
        from django.utils import timezone
        updated = queryset.update(status='answered', answered_by=request.user, answered_at=timezone.now())
        self.message_user(request, f'{updated} message(s) marqué(s) comme répondu(s).')
    mark_as_answered.short_description = '💬 Marquer comme répondu'
    
    def mark_as_archived(self, request, queryset):
        """Archiver les messages"""
        updated = queryset.update(status='archived')
        self.message_user(request, f'{updated} message(s) archivé(s).')
    mark_as_archived.short_description = '📦 Archiver'
    
    def delete_selected_messages(self, request, queryset):
        """Supprimer les messages sélectionnés"""
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f'{count} message(s) supprimé(s).')
    delete_selected_messages.short_description = '🗑️ Supprimer définitivement'
    
    def get_queryset(self, request):
        """Personnaliser l'affichage par défaut"""
        qs = super().get_queryset(request)
        return qs
    
    class Media:
        css = {
            'all': ('admin/css/custom.css',)
        }


@admin.register(ChurchSettings)
class ChurchSettingsAdmin(admin.ModelAdmin):
    """Admin pour la gestion des paramètres globaux de l'église"""
    list_display = ['church_name', 'city', 'country', 'preview_contact', 'has_social_links', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('church_name', 'church_slogan', 'logo', 'favicon'),
            'description': 'Nom, slogan et identité visuelle de l\'église'
        }),
        ('Adresse', {
            'fields': ('address', 'city', 'country'),
            'classes': ('wide',)
        }),
        ('Contacts', {
            'fields': ('phone_primary', 'phone_secondary', 'email_primary', 'email_secondary'),
            'description': 'Informations de contact affichées sur le site'
        }),
        ('Horaires de bureau', {
            'fields': ('office_hours_weekdays', 'office_hours_saturday', 'office_hours_sunday'),
            'classes': ('wide',)
        }),
        ('Réseaux sociaux', {
            'fields': ('facebook_url', 'youtube_url', 'instagram_url', 'twitter_url', 'whatsapp_number', 'telegram_url'),
            'classes': ('collapse',)
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def preview_contact(self, obj):
        """Affiche un aperçu des informations de contact"""
        return format_html(
            '<div style="font-size: 12px;">'
            '<strong>📞</strong> {}<br>'
            '<strong>📞</strong> {}<br>'
            '<strong>✉️</strong> {}'
            '</div>',
            obj.phone_primary or '-',
            obj.phone_secondary or '-',
            obj.email_primary or '-'
        )
    preview_contact.short_description = 'Contacts'
    
    def has_social_links(self, obj):
        """Indique si des liens sociaux sont configurés"""
        links = []
        if obj.facebook_url:
            links.append('FB')
        if obj.youtube_url:
            links.append('YT')
        if obj.instagram_url:
            links.append('IG')
        if obj.twitter_url:
            links.append('TW')
        if obj.whatsapp_number:
            links.append('WA')
        if obj.telegram_url:
            links.append('TG')
        return format_html(
            '<span style="color: {};">{}</span>',
            '#22c55e' if links else '#ef4444',
            ', '.join(links) if links else 'Aucun'
        )
    has_social_links.short_description = 'Réseaux sociaux'
    
    def has_add_permission(self, request):
        """Empêcher la création de plusieurs instances"""
        if ChurchSettings.objects.exists():
            return False
        return super().has_add_permission(request)
    
    def has_delete_permission(self, request, obj=None):
        """Empêcher la suppression des paramètres"""
        return False
    
    def get_queryset(self, request):
        """Personnaliser l'affichage par défaut"""
        qs = super().get_queryset(request)
        return qs
