"""
Tests for permissions module.
"""
import pytest
from rest_framework import status
from django.contrib.auth.models import AnonymousUser

from church_management.permissions import (
    IsAdminOrSuperAdmin,
    IsSecretaryOrAdmin,
    IsTreasurerOrAdmin,
    IsLogisticsHeadOrAdmin,
    PublicReadAdminWrite
)


@pytest.mark.unit
class TestIsAdminOrSuperAdmin:
    """Tests for IsAdminOrSuperAdmin permission."""

    def test_superuser_has_permission(self, super_admin_user):
        """Test that superusers have permission."""
        from rest_framework.test import APIRequestFactory
        permission = IsAdminOrSuperAdmin()
        request = APIRequestFactory().get('/')
        request.user = super_admin_user
        assert permission.has_permission(request, None) is True

    def test_admin_has_permission(self, admin_user):
        """Test that admin users have permission."""
        from rest_framework.test import APIRequestFactory
        permission = IsAdminOrSuperAdmin()
        request = APIRequestFactory().get('/')
        request.user = admin_user
        assert permission.has_permission(request, None) is True

    def test_regular_user_no_permission(self, regular_user):
        """Test that regular users don't have permission."""
        from rest_framework.test import APIRequestFactory
        permission = IsAdminOrSuperAdmin()
        request = APIRequestFactory().get('/')
        request.user = regular_user
        assert permission.has_permission(request, None) is False


@pytest.mark.unit
class TestIsSecretaryOrAdmin:
    """Tests for IsSecretaryOrAdmin permission."""

    def test_secretary_has_permission(self, secretary_user):
        """Test that secretaries have permission."""
        from rest_framework.test import APIRequestFactory
        permission = IsSecretaryOrAdmin()
        request = APIRequestFactory().get('/')
        request.user = secretary_user
        assert permission.has_permission(request, None) is True

    def test_admin_has_permission(self, admin_user):
        """Test that admins have permission."""
        from rest_framework.test import APIRequestFactory
        permission = IsSecretaryOrAdmin()
        request = APIRequestFactory().get('/')
        request.user = admin_user
        assert permission.has_permission(request, None) is True


@pytest.mark.unit
class TestIsTreasurerOrAdmin:
    """Tests for IsTreasurerOrAdmin permission."""

    def test_treasurer_has_permission(self, treasurer_user):
        """Test that treasurers have permission."""
        from rest_framework.test import APIRequestFactory
        permission = IsTreasurerOrAdmin()
        request = APIRequestFactory().get('/')
        request.user = treasurer_user
        assert permission.has_permission(request, None) is True


@pytest.mark.unit
class TestIsLogisticsHeadOrAdmin:
    """Tests for IsLogisticsHeadOrAdmin permission."""

    def test_logistics_head_has_permission(self, logistics_head_user):
        """Test that logistics heads have permission."""
        from rest_framework.test import APIRequestFactory
        permission = IsLogisticsHeadOrAdmin()
        request = APIRequestFactory().get('/')
        request.user = logistics_head_user
        assert permission.has_permission(request, None) is True


@pytest.mark.unit
class TestPublicReadAdminWrite:
    """Tests for PublicReadAdminWrite permission."""

    def test_anonymous_can_read(self):
        """Test that anonymous users can read."""
        from rest_framework.test import APIRequestFactory
        permission = PublicReadAdminWrite()
        request = APIRequestFactory().get('/')
        request.user = AnonymousUser()
        request.method = 'GET'
        assert permission.has_permission(request, None) is True

    def test_anonymous_cannot_write(self):
        """Test that anonymous users cannot write."""
        from rest_framework.test import APIRequestFactory
        permission = PublicReadAdminWrite()
        request = APIRequestFactory().post('/')
        request.user = AnonymousUser()
        request.method = 'POST'
        assert permission.has_permission(request, None) is False

    def test_admin_can_write(self, admin_user):
        """Test that admins can write."""
        from rest_framework.test import APIRequestFactory
        permission = PublicReadAdminWrite()
        request = APIRequestFactory().post('/')
        request.user = admin_user
        request.method = 'POST'
        assert permission.has_permission(request, None) is True
