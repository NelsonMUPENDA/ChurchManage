# church_management_app/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import api
from . import views

# Create router for API endpoints
router = DefaultRouter()
router.register(r'members', api.MemberViewSet, basename='members')
router.register(r'events', api.EventViewSet, basename='events')
router.register(r'announcements', api.AnnouncementViewSet, basename='announcements')
router.register(r'financial-transactions', api.FinancialTransactionViewSet, basename='financial-transactions')
router.register(r'attendance', api.AttendanceViewSet, basename='attendance')
router.register(r'marriages', api.MarriageRecordViewSet, basename='marriages')
router.register(r'evangelism-activities', api.EvangelismActivityViewSet, basename='evangelism-activities')
router.register(r'logistics-items', api.LogisticsItemViewSet, basename='logistics-items')

urlpatterns = [
    # API URLs
    path('api/', include(router.urls)),
    path('api/auth/', include('rest_framework.urls')),
    # JWT Authentication endpoints
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/dashboard/summary/', api.DashboardSummaryView.as_view(), name='dashboard-summary'),
    path('api/me/', api.MeView.as_view(), name='current-user'),
    
    # Frontend URLs - Using views functions
    path('', views.index, name='home'),
    path('login/', views.login_page, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('members/', views.members, name='members'),
    path('member-detail/<int:pk>/', views.member_detail, name='member-detail'),
    path('events/', views.events, name='events'),
    path('event-detail/<int:pk>/', views.event_detail, name='event-detail'),
    path('finances/', views.finances, name='finances'),
    path('reports/', views.reports, name='reports'),
    path('announcements/', views.announcements, name='announcements'),
    path('diaconat/', views.diaconat, name='diaconat'),
    path('evangelisation/', views.evangelisation, name='evangelisation'),
    path('mariage/', views.mariage, name='mariage'),
    path('account/', views.account, name='account'),
    path('about/', views.public_about, name='about'),
    path('contact/', views.contact, name='contact'),
]
