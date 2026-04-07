"""
Tests for core API endpoints: MeView, DashboardSummaryView, UserViewSet.
"""
import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.unit
class TestMeView:
    """Tests for the /api/me/ endpoint."""

    def test_me_unauthenticated(self, api_client):
        """Test that unauthenticated requests are rejected."""
        response = api_client.get('/api/me/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_me_authenticated(self, authenticated_client):
        """Test that authenticated users can retrieve their profile."""
        response = authenticated_client.get('/api/me/')
        assert response.status_code == status.HTTP_200_OK
        assert 'username' in response.data
        assert response.data['username'] == authenticated_client.user.username

    def test_me_update_profile(self, authenticated_client):
        """Test that users can update their profile."""
        data = {
            'first_name': 'Updated',
            'last_name': 'Name'
        }
        response = authenticated_client.post('/api/me/', data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['first_name'] == 'Updated'

    def test_me_update_phone(self, authenticated_client):
        """Test updating phone number."""
        data = {'phone': '+243999999999'}
        response = authenticated_client.post('/api/me/', data)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.unit
class TestDashboardSummaryView:
    """Tests for the /api/dashboard/summary/ endpoint."""

    def test_dashboard_unauthenticated(self, api_client):
        """Test that unauthenticated requests are rejected."""
        response = api_client.get('/api/dashboard/summary/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_dashboard_admin_access(self, admin_client):
        """Test that admins can access dashboard."""
        response = admin_client.get('/api/dashboard/summary/')
        assert response.status_code == status.HTTP_200_OK
        assert 'members' in response.data
        assert 'events' in response.data

    def test_dashboard_secretary_access(self, api_client, secretary_user):
        """Test that secretaries can access relevant dashboard data."""
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(secretary_user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        response = api_client.get('/api/dashboard/summary/')
        assert response.status_code == status.HTTP_200_OK
        # Secretaries should see members and events
        assert 'members' in response.data
        assert 'events' in response.data

    def test_dashboard_treasurer_access(self, api_client, treasurer_user):
        """Test that treasurers can access financial dashboard data."""
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(treasurer_user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        response = api_client.get('/api/dashboard/summary/')
        assert response.status_code == status.HTTP_200_OK
        assert 'finances' in response.data

    def test_dashboard_logistics_access(self, api_client, logistics_head_user):
        """Test that logistics heads can access logistics dashboard data."""
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(logistics_head_user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        response = api_client.get('/api/dashboard/summary/')
        assert response.status_code == status.HTTP_200_OK
        assert 'logistics' in response.data


@pytest.mark.unit
class TestUserViewSet:
    """Tests for the /api/users/ endpoint."""

    def test_list_users_admin(self, admin_client):
        """Test that admins can list users."""
        response = admin_client.get('/api/users/')
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)

    def test_list_users_regular_user(self, authenticated_client):
        """Test that regular users cannot list users."""
        response = authenticated_client.get('/api/users/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_user_admin(self, admin_client):
        """Test that admins can create users."""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'role': 'member'
        }
        response = admin_client.post('/api/users/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['username'] == 'newuser'

    def test_block_user_admin(self, admin_client, create_user):
        """Test that admins can block users."""
        user = create_user(username='toblock')
        response = admin_client.post(f'/api/users/{user.id}/block/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['is_active'] is False

    def test_unblock_user_admin(self, admin_client, create_user):
        """Test that admins can unblock users."""
        user = create_user(username='tounblock', is_active=False)
        response = admin_client.post(f'/api/users/{user.id}/unblock/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['is_active'] is True

    def test_block_user_unauthorized(self, authenticated_client, create_user):
        """Test that regular users cannot block users."""
        user = create_user(username='toblock2')
        response = authenticated_client.post(f'/api/users/{user.id}/block/')
        assert response.status_code == status.HTTP_403_FORBIDDEN
