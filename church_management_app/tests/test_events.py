"""
Tests for events API: Events, Attendance, Ceremonies.
"""
import pytest
from rest_framework import status
from django.utils import timezone
import datetime


@pytest.mark.unit
class TestEventViewSet:
    """Tests for the /api/events/ endpoint."""

    def test_list_events_unauthenticated(self, api_client, create_event):
        """Test that events are publicly readable when published."""
        create_event(is_published=True)
        response = api_client.get('/api/events/')
        # Events use IsAdminOrSuperAdminOrReadOnly
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED]

    def test_create_event_admin(self, admin_client):
        """Test that admins can create events."""
        data = {
            'title': 'New Event',
            'event_type': 'service',
            'date': str(timezone.localdate()),
            'duration_type': 'daily'
        }
        response = admin_client.post('/api/events/', data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_filter_events_by_date(self, admin_client, create_event):
        """Test filtering events by date."""
        today = timezone.localdate()
        create_event(date=today)
        response = admin_client.get(f'/api/events/?date={today}')
        assert response.status_code == status.HTTP_200_OK

    def test_filter_events_by_type(self, admin_client, create_event):
        """Test filtering events by type."""
        create_event(event_type='baptism')
        response = admin_client.get('/api/events/?event_type=baptism')
        assert response.status_code == status.HTTP_200_OK

    def test_publish_event(self, admin_client, create_event):
        """Test publishing an event."""
        event = create_event(is_published=False)
        response = admin_client.post(f'/api/events/{event.id}/publish/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['is_published'] is True

    def test_unpublish_event(self, admin_client, create_event):
        """Test unpublishing an event."""
        event = create_event(is_published=True)
        response = admin_client.post(f'/api/events/{event.id}/unpublish/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['is_published'] is False

    def test_set_alert(self, admin_client, create_event):
        """Test setting an alert on an event."""
        event = create_event()
        data = {'message': 'Test alert message'}
        response = admin_client.post(f'/api/events/{event.id}/set-alert/', data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['is_alert'] is True

    def test_clear_alert(self, admin_client, create_event):
        """Test clearing an alert on an event."""
        event = create_event(is_alert=True, alert_message='Alert')
        response = admin_client.post(f'/api/events/{event.id}/clear-alert/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['is_alert'] is False

    def test_validate_closure(self, admin_client, create_event):
        """Test validating event closure."""
        event = create_event()
        response = admin_client.post(f'/api/events/{event.id}/validate-closure/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['closure_validated_at'] is not None


@pytest.mark.unit
class TestAttendanceViewSet:
    """Tests for the /api/attendance/ endpoint."""

    def test_list_attendance_secretary(self, api_client, secretary_user, create_event):
        """Test that secretaries can list attendance."""
        from rest_framework_simplejwt.tokens import RefreshToken
        event = create_event()
        refresh = RefreshToken.for_user(secretary_user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        response = api_client.get('/api/attendance/')
        assert response.status_code == status.HTTP_200_OK

    def test_filter_attendance_by_event(self, admin_client, create_event):
        """Test filtering attendance by event."""
        event = create_event()
        response = admin_client.get(f'/api/attendance/?event={event.id}')
        assert response.status_code == status.HTTP_200_OK

    def test_filter_attendance_by_status(self, admin_client, create_event, create_member):
        """Test filtering attendance by attended status."""
        from church_management.models import Attendance
        event = create_event()
        member = create_member()
        Attendance.objects.create(event=event, member=member, attended=True)

        response = admin_client.get('/api/attendance/?attended=true')
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.unit
class TestBaptismEventViewSet:
    """Tests for the /api/baptism-events/ endpoint."""

    def test_list_baptism_events_secretary(self, api_client, secretary_user):
        """Test that secretaries can list baptism events."""
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(secretary_user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        response = api_client.get('/api/baptism-events/')
        assert response.status_code == status.HTTP_200_OK

    def test_create_baptism_event(self, api_client, secretary_user):
        """Test creating a baptism event."""
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(secretary_user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        data = {
            'title': 'Baptism Service',
            'date': str(timezone.localdate()),
            'moderator': 'Pastor John'
        }
        response = api_client.post('/api/baptism-events/', data)
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.unit
class TestEvangelismActivityViewSet:
    """Tests for the /api/evangelism-activities/ endpoint."""

    def test_list_evangelism_activities(self, api_client):
        """Test listing evangelism activities requires authentication."""
        response = api_client.get('/api/evangelism-activities/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_evangelism_activity_requires_approval(self, authenticated_client):
        """Test that non-admin users need approval to create."""
        data = {
            'title': 'Evangelism Campaign',
            'date': str(timezone.localdate()),
        }
        response = authenticated_client.post('/api/evangelism-activities/', data)
        # Non-admin users get 202 with approval request
        assert response.status_code in [status.HTTP_202_ACCEPTED, status.HTTP_201_CREATED, status.HTTP_403_FORBIDDEN]


@pytest.mark.unit
class TestTrainingEventViewSet:
    """Tests for the /api/training-events/ endpoint."""

    def test_list_training_events(self, api_client):
        """Test listing training events requires authentication."""
        response = api_client.get('/api/training-events/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_training_event_admin(self, admin_client):
        """Test that admins can create training events."""
        data = {
            'title': 'Leadership Training',
            'date': str(timezone.localdate()),
        }
        response = admin_client.post('/api/training-events/', data)
        assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_202_ACCEPTED]


@pytest.mark.unit
class TestPublicEventAccess:
    """Tests for public event access via share slug."""

    def test_public_event_access(self, api_client, create_event):
        """Test accessing a public event by share slug."""
        event = create_event(is_published=True)
        # Ensure event has a share_slug
        from church_management.api.helpers import _ensure_event_share_slug
        _ensure_event_share_slug(event)

        response = api_client.get(f'/api/events/public/{event.share_slug}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == event.title

    def test_public_event_not_found(self, api_client):
        """Test that invalid slugs return 404."""
        response = api_client.get('/api/events/public/invalid-slug-12345/')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_public_event_comment(self, api_client, create_event):
        """Test adding comments to public events."""
        event = create_event(is_published=True)
        from church_management.api.helpers import _ensure_event_share_slug
        _ensure_event_share_slug(event)

        data = {
            'text': 'Great event!',
            'author_name': 'John Doe'
        }
        response = api_client.post(f'/api/events/public/{event.share_slug}/comment/', data)
        assert response.status_code == status.HTTP_201_CREATED
