# church_management_app/urls.py - URLs Django
from django.urls import path
from . import views
from .views_user_management import user_management, user_create_admin, user_created_success, user_edit_admin, user_delete_admin, user_toggle_active

urlpatterns = [
    # Page d'accueil
    path('', views.index, name='home'),
    
    # Authentification
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Tableau de bord
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Membres - CRUD
    path('members/', views.member_list, name='member-list'),
    path('members/create/', views.member_create, name='member-create'),
    path('members/<int:pk>/', views.member_detail, name='member-detail'),
    path('members/<int:pk>/edit/', views.member_edit, name='member-edit'),
    path('members/<int:pk>/delete/', views.member_delete, name='member-delete'),
    path('members/print/', views.member_print_list, name='member-print-list'),
    path('members/print-preview/', views.member_print_preview, name='member-print-preview'),
    path('members/export/', views.member_export, name='member-export'),
    path('members/<int:pk>/print-card/', views.member_print_card, name='member-print-card'),
    path('members/<int:pk>/profile-print/', views.member_profile_print, name='member-profile-print'),
    
    # Familles - CRUD
    path('families/', views.family_list, name='family-list'),
    path('families/create/', views.family_create, name='family-create'),
    path('families/<int:pk>/edit/', views.family_edit, name='family-edit'),
    path('families/<int:pk>/delete/', views.family_delete, name='family-delete'),
    
    # Groupes de maison - CRUD
    path('home-groups/', views.homegroup_list, name='homegroup-list'),
    path('home-groups/create/', views.homegroup_create, name='homegroup-create'),
    path('home-groups/<int:pk>/edit/', views.homegroup_edit, name='homegroup-edit'),
    path('home-groups/<int:pk>/delete/', views.homegroup_delete, name='homegroup-delete'),
    
    # Départements - CRUD
    path('departments/', views.department_list, name='department-list'),
    path('departments/create/', views.department_create, name='department-create'),
    path('departments/<int:pk>/edit/', views.department_edit, name='department-edit'),
    path('departments/<int:pk>/delete/', views.department_delete, name='department-delete'),
    
    # Ministères - CRUD
    path('ministries/', views.ministry_list, name='ministry-list'),
    path('ministries/create/', views.ministry_create, name='ministry-create'),
    path('ministries/<int:pk>/edit/', views.ministry_edit, name='ministry-edit'),
    path('ministries/<int:pk>/delete/', views.ministry_delete, name='ministry-delete'),
    
    # Événements - CRUD
    path('events/', views.event_list, name='event-list'),
    path('events/create/', views.event_create, name='event-create'),
    path('events/<int:pk>/', views.event_detail, name='event-detail'),
    path('events/<int:pk>/edit/', views.event_edit, name='event-edit'),
    path('events/<int:pk>/delete/', views.event_delete, name='event-delete'),
    
    # Présences (Pointage)
    path('attendance/', views.attendance_list, name='attendance-list'),
    path('attendance/event/<int:event_pk>/', views.attendance_event, name='attendance-event'),
    
    # Finances - CRUD
    path('finances/', views.finance_list, name='finance-list'),
    path('finances/<int:pk>/', views.transaction_detail, name='transaction-detail'),
    path('finances/transactions/create/', views.transaction_create, name='transaction-create'),
    path('finances/transactions/<int:pk>/edit/', views.transaction_edit, name='transaction-edit'),
    path('finances/transactions/<int:pk>/delete/', views.transaction_delete, name='transaction-delete'),
    path('finances/categories/', views.category_list, name='category-list'),
    path('finances/categories/create/', views.category_create, name='category-create'),
    path('finances/categories/<int:pk>/edit/', views.category_edit, name='category-edit'),
    path('finances/categories/<int:pk>/delete/', views.category_delete, name='category-delete'),
    
    # Rapports
    path('reports/', views.reports, name='reports'),
    
    # Annonces - CRUD
    path('announcements/', views.announcement_list, name='announcement-list'),
    path('announcements/create/', views.announcement_create, name='announcement-create'),
    path('announcements/<int:pk>/', views.announcement_detail, name='announcement-detail'),
    path('announcements/<int:pk>/edit/', views.announcement_edit, name='announcement-edit'),
    path('announcements/<int:pk>/delete/', views.announcement_delete, name='announcement-delete'),
    
    # Diaconat (Pointage et Logistique)
    path('diaconat/', views.diaconat, name='diaconat'),
    path('diaconat/attendance/', views.diaconat_attendance, name='diaconat-attendance'),

    # Logistique - CRUD (alias sous diaconat pour cohérence)
    path('diaconat/logistics/create/', views.logistics_create, name='diaconat-logistics-create'),
    path('diaconat/logistics/<int:pk>/', views.logistics_detail, name='diaconat-logistics-detail'),
    path('diaconat/logistics/<int:pk>/edit/', views.logistics_edit, name='diaconat-logistics-edit'),
    path('diaconat/logistics/<int:pk>/delete/', views.logistics_delete, name='diaconat-logistics-delete'),

    # Logistique - AJAX pour catégories et états dynamiques
    path('diaconat/logistics/category/create-ajax/', views.logistics_create_category_ajax, name='logistics-category-ajax'),
    path('diaconat/logistics/condition/create-ajax/', views.logistics_create_condition_ajax, name='logistics-condition-ajax'),

    # Logistique - CRUD (URLs originales)
    path('logistics/', views.logistics_list, name='logistics-list'),
    path('logistics/<int:pk>/', views.logistics_detail, name='logistics-detail'),
    path('logistics/create/', views.logistics_create, name='logistics-create'),
    path('logistics/<int:pk>/edit/', views.logistics_edit, name='logistics-edit'),
    path('logistics/<int:pk>/delete/', views.logistics_delete, name='logistics-delete'),
    
    # Évangélisation - CRUD
    path('evangelisation/', views.evangelisation_list, name='evangelisation-list'),
    path('evangelisation/create/', views.evangelisation_create, name='evangelisation-create'),
    path('evangelisation/<int:pk>/edit/', views.evangelisation_edit, name='evangelisation-edit'),
    path('evangelisation/<int:pk>/delete/', views.evangelisation_delete, name='evangelisation-delete'),
    
    # Formations - CRUD
    path('trainings/', views.training_list, name='training-list'),
    path('trainings/create/', views.training_create, name='training-create'),
    path('trainings/<int:pk>/edit/', views.training_edit, name='training-edit'),
    path('trainings/<int:pk>/delete/', views.training_delete, name='training-delete'),
    
    # Mariages - CRUD
    path('marriages/', views.marriage_list, name='marriage-list'),
    path('marriages/create/', views.marriage_create, name='marriage-create'),
    path('marriages/<int:pk>/', views.marriage_detail, name='marriage-detail'),
    path('marriages/<int:pk>/edit/', views.marriage_edit, name='marriage-edit'),
    path('marriages/<int:pk>/delete/', views.marriage_delete, name='marriage-delete'),
    
    # Documents - CRUD
    path('documents/', views.document_list, name='document-list'),
    path('documents/create/', views.document_create, name='document-create'),
    path('documents/<int:pk>/', views.document_detail, name='document-detail'),
    path('documents/<int:pk>/edit/', views.document_edit, name='document-edit'),
    path('documents/<int:pk>/delete/', views.document_delete, name='document-delete'),
    
    # Compte utilisateur
    path('account/', views.account, name='account'),
    path('account/edit/', views.account_edit, name='account-edit'),
    
    # Gestion des utilisateurs système (Admin)
    path('account/users/', user_management, name='user-management'),
    path('account/users/create/', user_create_admin, name='user-create-admin'),
    path('account/users/created/', user_created_success, name='user-created-success'),
    path('account/users/<int:pk>/edit/', user_edit_admin, name='user-edit-admin'),
    path('account/users/<int:pk>/delete/', user_delete_admin, name='user-delete-admin'),
    path('account/users/<int:pk>/toggle/', user_toggle_active, name='user-toggle-active'),

    # Baptêmes - CRUD
    path('baptisms/', views.baptism_list, name='baptism-list'),
    path('baptisms/create/', views.baptism_create, name='baptism-create'),
    path('baptisms/<int:pk>/', views.baptism_detail, name='baptism-detail'),
    path('baptisms/<int:pk>/edit/', views.baptism_edit, name='baptism-edit'),
    path('baptisms/<int:pk>/delete/', views.baptism_delete, name='baptism-delete'),
    path('baptisms/<int:pk>/candidates/add/', views.baptism_candidate_add, name='baptism-candidate-add'),

    # Contact Admin (gestion des messages reçus)
    path('management/contacts/', views.contact_admin_list, name='contact-admin-list'),
    path('management/contacts/<int:pk>/', views.contact_admin_detail, name='contact-admin-detail'),
    path('management/contacts/<int:pk>/mark-read/', views.contact_mark_read, name='contact-mark-read'),
    path('management/contacts/<int:pk>/archive/', views.contact_archive, name='contact-archive'),

    # Audit Logs (Logs système)
    path('management/audit-logs/', views.audit_log_list, name='audit-log-list'),

    # Demandes d'approbation
    path('approval-requests/', views.approval_request_list, name='approval-request-list'),
    path('approval-requests/<int:pk>/', views.approval_request_detail, name='approval-request-detail'),
    path('approval-requests/<int:pk>/approve/', views.approval_request_approve, name='approval-request-approve'),
    path('approval-requests/<int:pk>/reject/', views.approval_request_reject, name='approval-request-reject'),

    # Rapports détaillés
    path('reports/members/', views.report_members_detail, name='report-members-detail'),
    path('reports/finances/', views.report_finances_detail, name='report-finances-detail'),
    path('reports/activities/', views.report_activities_detail, name='report-activities-detail'),
    path('reports/attendance/', views.report_attendance_detail, name='report-attendance-detail'),
    path('reports/sacraments/', views.report_sacraments_detail, name='report-sacraments-detail'),
    path('reports/export-excel/', views.export_reports_excel, name='reports-export-excel'),
    path('reports/export-pdf/<str:report_type>/', views.export_report_pdf, name='reports-export-pdf'),

    # Notifications
    path('notifications/', views.notification_list, name='notification-list'),
    path('notifications/<int:pk>/mark-read/', views.notification_mark_read, name='notification-mark-read'),
    path('notifications/mark-all-read/', views.notification_mark_all_read, name='notification-mark-all-read'),
    path('notifications/<int:pk>/delete/', views.notification_delete, name='notification-delete'),

    # Paramètres de l'église
    path('settings/', views.church_settings_view, name='church-settings'),
    path('settings/biography/', views.church_biography_view, name='church-biography'),
    path('settings/activities/', views.church_activities_view, name='church-activities'),
    path('settings/activities/create/', views.activity_create_view, name='activity-create'),
    path('settings/activities/<int:pk>/edit/', views.activity_edit_view, name='activity-edit'),
    path('settings/activities/<int:pk>/delete/', views.activity_delete_view, name='activity-delete'),
    path('settings/services/', views.church_services_view, name='church-services'),
    path('settings/services/create/', views.service_create_view, name='service-create'),
    path('settings/services/<int:pk>/edit/', views.service_edit_view, name='service-edit'),
    path('settings/services/<int:pk>/delete/', views.service_delete_view, name='service-delete'),

    # AJAX Endpoints pour création dynamique
    path('ajax/family/create/', views.ajax_create_family, name='ajax-create-family'),
    path('ajax/department/create/', views.ajax_create_department, name='ajax-create-department'),
    path('ajax/ministry/create/', views.ajax_create_ministry, name='ajax-create-ministry'),

    # Pages publiques
    path('about/', views.public_about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('calendar/', views.public_events, name='public-events'),
]
