"""
Pytest configuration and shared fixtures for church_management tests.
"""
import pytest
import uuid
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from church_management.models import (
    Member, Family, HomeGroup, Department, Ministry,
    Event, FinancialCategory, LogisticsItem, Announcement
)

User = get_user_model()


@pytest.fixture
def api_client():
    """Return an unauthenticated API client."""
    return APIClient()


@pytest.fixture
def create_user(db):
    """Factory fixture to create users with different roles."""
    counter = 0
    def _create_user(
        username=None,
        email=None,
        password='testpass123',
        role='member',
        is_staff=False,
        is_superuser=False,
        **kwargs
    ):
        nonlocal counter
        counter += 1
        unique_id = str(uuid.uuid4())[:8]
        if username is None:
            username = f'user_{unique_id}_{counter}'
        if email is None:
            email = f'{username}@example.com'
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **kwargs
        )
        return user
    return _create_user


@pytest.fixture
def admin_user(create_user):
    """Create an admin user."""
    return create_user(
        role='admin',
        is_staff=True
    )


@pytest.fixture
def super_admin_user(create_user):
    """Create a super admin user."""
    return create_user(
        role='super_admin',
        is_staff=True,
        is_superuser=True
    )


@pytest.fixture
def secretary_user(create_user):
    """Create a secretary user."""
    return create_user(
        role='secretary'
    )


@pytest.fixture
def treasurer_user(create_user):
    """Create a treasurer user."""
    return create_user(
        role='treasurer'
    )


@pytest.fixture
def logistics_head_user(create_user):
    """Create a logistics head user."""
    return create_user(
        role='logistics_head'
    )


@pytest.fixture
def regular_user(create_user):
    """Create a regular member user."""
    return create_user(
        role='member'
    )


@pytest.fixture
def authenticated_client(api_client, create_user):
    """Return an authenticated API client for a regular user."""
    user = create_user()
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    api_client.user = user
    return api_client


@pytest.fixture
def admin_client(api_client, admin_user):
    """Return an authenticated API client for an admin user."""
    refresh = RefreshToken.for_user(admin_user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    api_client.user = admin_user
    return api_client


@pytest.fixture
def super_admin_client(api_client, super_admin_user):
    """Return an authenticated API client for a super admin user."""
    refresh = RefreshToken.for_user(super_admin_user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    api_client.user = super_admin_user
    return api_client


@pytest.fixture
def create_department(db):
    """Factory to create departments."""
    def _create_department(name='Test Department', description='Test description'):
        return Department.objects.create(name=name, description=description)
    return _create_department


@pytest.fixture
def create_family(db):
    """Factory to create families."""
    def _create_family(name='Test Family'):
        return Family.objects.create(name=name)
    return _create_family


@pytest.fixture
def create_home_group(db):
    """Factory to create home groups."""
    def _create_home_group(name='Test Group', **kwargs):
        return HomeGroup.objects.create(name=name, **kwargs)
    return _create_home_group


@pytest.fixture
def create_member(db, create_user, create_family, create_home_group, create_department):
    """Factory to create members."""
    def _create_member(
        user=None,
        family=None,
        home_group=None,
        department=None,
        gender='M',
        **kwargs
    ):
        if user is None:
            user = create_user(username=f'member_{Member.objects.count()}')
        if family is None:
            family = create_family()
        if home_group is None:
            home_group = create_home_group()
        if department is None:
            department = Department.objects.create(name=f'Dept {Department.objects.count()}')

        return Member.objects.create(
            user=user,
            family=family,
            home_group=home_group,
            department=department,
            gender=gender,
            **kwargs
        )
    return _create_member


@pytest.fixture
def create_event(db):
    """Factory to create events."""
    def _create_event(
        title='Test Event',
        event_type='service',
        date=None,
        **kwargs
    ):
        from django.utils import timezone
        import datetime
        if date is None:
            date = timezone.localdate()
        return Event.objects.create(
            title=title,
            event_type=event_type,
            date=date,
            **kwargs
        )
    return _create_event


@pytest.fixture
def create_financial_category(db):
    """Factory to create financial categories."""
    def _create_category(name='Test Category', category_type='income'):
        return FinancialCategory.objects.create(
            name=name,
            category_type=category_type
        )
    return _create_category


@pytest.fixture
def create_logistics_item(db):
    """Factory to create logistics items."""
    def _create_item(name='Test Item', quantity=10, **kwargs):
        return LogisticsItem.objects.create(
            name=name,
            quantity=quantity,
            **kwargs
        )
    return _create_item


@pytest.fixture
def create_announcement(db, admin_user):
    """Factory to create announcements."""
    def _create_announcement(
        title='Test Announcement',
        content='Test content',
        author=None,
        **kwargs
    ):
        if author is None:
            author = admin_user
        return Announcement.objects.create(
            title=title,
            content=content,
            author=author,
            **kwargs
        )
    return _create_announcement
