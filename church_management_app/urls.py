# church_management_app/urls.py - URLs Django traditionnelles (sans API)
from django.urls import path
from . import views

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
    
    # Logistique - CRUD
    path('logistics/', views.logistics_list, name='logistics-list'),
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
    path('documents/<int:pk>/delete/', views.document_delete, name='document-delete'),
    
    # Compte utilisateur
    path('account/', views.account, name='account'),
    path('account/edit/', views.account_edit, name='account-edit'),
    
    # Pages publiques
    path('about/', views.public_about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('calendar/', views.public_events, name='public-events'),
]
