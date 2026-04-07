"""
Tests for content API: Announcements, AnnouncementDecks, Documents, ChurchBiography, ChurchConsistory.
"""
import pytest
from rest_framework import status
from django.utils import timezone


@pytest.mark.unit
class TestAnnouncementViewSet:
    """Tests for the /api/announcements/ endpoint."""

    def test_list_announcements_public(self, api_client, create_announcement):
        """Test that announcements are publicly readable."""
        create_announcement()
        response = api_client.get('/api/announcements/')
        assert response.status_code == status.HTTP_200_OK

    def test_create_announcement_admin(self, admin_client):
        """Test that admins can create announcements."""
        data = {
            'title': 'New Announcement',
            'content': 'Announcement content',
        }
        response = admin_client.post('/api/announcements/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == 'New Announcement'

    def test_create_announcement_unauthorized(self, authenticated_client):
        """Test that regular users cannot create announcements."""
        data = {
            'title': 'New Announcement',
            'content': 'Announcement content',
        }
        response = authenticated_client.post('/api/announcements/', data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_like_announcement(self, authenticated_client, create_announcement):
        """Test liking an announcement."""
        announcement = create_announcement()
        response = authenticated_client.post(f'/api/announcements/{announcement.id}/like/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['liked'] is True

    def test_unlike_announcement(self, authenticated_client, create_announcement):
        """Test unliking an announcement (second click)."""
        from church_management.models import AnnouncementLike
        announcement = create_announcement()
        AnnouncementLike.objects.create(announcement=announcement, user=authenticated_client.user)

        response = authenticated_client.post(f'/api/announcements/{announcement.id}/like/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['liked'] is False

    def test_list_comments(self, authenticated_client, create_announcement):
        """Test listing comments on an announcement."""
        announcement = create_announcement()
        response = authenticated_client.get(f'/api/announcements/{announcement.id}/comments/')
        assert response.status_code == status.HTTP_200_OK

    def test_add_comment(self, authenticated_client, create_announcement):
        """Test adding a comment to an announcement."""
        announcement = create_announcement()
        data = {'text': 'Great announcement!'}
        response = authenticated_client.post(f'/api/announcements/{announcement.id}/comments/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['text'] == 'Great announcement!'

    def test_like_comment(self, authenticated_client, create_announcement):
        """Test liking a comment on an announcement."""
        from church_management.models import AnnouncementComment
        announcement = create_announcement()
        comment = AnnouncementComment.objects.create(
            announcement=announcement,
            author=authenticated_client.user,
            text='Test comment'
        )

        response = authenticated_client.post(f'/api/announcements/{announcement.id}/comments/{comment.id}/like/')
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.unit
class TestAnnouncementDeckViewSet:
    """Tests for the /api/announcement-decks/ endpoint."""

    def test_list_decks_admin(self, admin_client):
        """Test that admins can list announcement decks."""
        response = admin_client.get('/api/announcement-decks/')
        assert response.status_code == status.HTTP_200_OK

    def test_create_deck_admin(self, admin_client, create_event):
        """Test that admins can create announcement decks."""
        event = create_event()
        data = {
            'title': 'Sunday Service Deck',
            'event': event.id,
            'header_text': 'Welcome to church'
        }
        response = admin_client.post('/api/announcement-decks/', data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_set_items(self, admin_client):
        """Test setting deck items."""
        from church_management.models import AnnouncementDeck
        deck = AnnouncementDeck.objects.create(title='Test Deck', created_by=admin_client.user)

        data = {
            'items': [
                {'order': 1, 'text': 'First announcement'},
                {'order': 2, 'text': 'Second announcement'}
            ]
        }
        response = admin_client.post(f'/api/announcement-decks/{deck.id}/set-items/', data)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2


@pytest.mark.unit
class TestDocumentViewSet:
    """Tests for the /api/documents/ endpoint."""

    def test_list_documents_admin(self, admin_client):
        """Test that admins can list documents."""
        response = admin_client.get('/api/documents/')
        assert response.status_code == status.HTTP_200_OK

    def test_create_document_admin(self, admin_client):
        """Test that admins can create documents."""
        data = {
            'title': 'Test Document',
            'description': 'Document description'
        }
        response = admin_client.post('/api/documents/', data)
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.unit
class TestChurchBiographyViewSet:
    """Tests for the /api/church-biography/ endpoint."""

    def test_list_biography_public(self, api_client, admin_client):
        """Test that church biography is publicly readable."""
        # Create a biography entry
        data = {
            'title': 'Church History',
            'content': 'Our church was founded in 1990...',
            'is_active': True
        }
        admin_client.post('/api/church-biography/', data)

        # Public read
        response = api_client.get('/api/church-biography/')
        assert response.status_code == status.HTTP_200_OK

    def test_create_biography_admin(self, admin_client):
        """Test that admins can create church biography entries."""
        data = {
            'title': 'Church History',
            'content': 'Our church was founded in 1990...',
            'is_active': True
        }
        response = admin_client.post('/api/church-biography/', data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_update_biography_admin(self, admin_client):
        """Test that admins can update church biography entries."""
        from church_management.models import ChurchBiography
        bio = ChurchBiography.objects.create(
            title='Old Title',
            content='Old content',
            is_active=True
        )

        data = {'title': 'Updated Title'}
        response = admin_client.patch(f'/api/church-biography/{bio.id}/', data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Updated Title'

    def test_soft_delete_biography(self, admin_client):
        """Test soft deletion of biography entries."""
        from church_management.models import ChurchBiography
        bio = ChurchBiography.objects.create(
            title='To Delete',
            content='Content to delete',
            is_active=True
        )

        response = admin_client.delete(f'/api/church-biography/{bio.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify it's soft deleted (not visible in active queryset)
        bio.refresh_from_db()
        assert bio.is_active is False


@pytest.mark.unit
class TestChurchConsistoryViewSet:
    """Tests for the /api/church-consistory/ endpoint."""

    def test_list_consistory_public(self, api_client, admin_client):
        """Test that church consistory is publicly readable."""
        # Create a consistory entry
        data = {
            'title': 'Pastoral Team',
            'content': 'Meet our pastoral team...',
            'is_active': True
        }
        admin_client.post('/api/church-consistory/', data)

        # Public read
        response = api_client.get('/api/church-consistory/')
        assert response.status_code == status.HTTP_200_OK

    def test_create_consistory_admin(self, admin_client):
        """Test that admins can create church consistory entries."""
        data = {
            'title': 'Pastoral Team',
            'content': 'Meet our pastoral team...',
            'is_active': True
        }
        response = admin_client.post('/api/church-consistory/', data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_update_consistory_admin(self, admin_client):
        """Test that admins can update church consistory entries."""
        from church_management.models import ChurchConsistory
        consistory = ChurchConsistory.objects.create(
            title='Old Title',
            content='Old content',
            is_active=True
        )

        data = {'title': 'Updated Title'}
        response = admin_client.patch(f'/api/church-consistory/{consistory.id}/', data)
        assert response.status_code == status.HTTP_200_OK

    def test_soft_delete_consistory(self, admin_client):
        """Test soft deletion of consistory entries."""
        from church_management.models import ChurchConsistory
        consistory = ChurchConsistory.objects.create(
            title='To Delete',
            content='Content to delete',
            is_active=True
        )

        response = admin_client.delete(f'/api/church-consistory/{consistory.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify it's soft deleted
        consistory.refresh_from_db()
        assert consistory.is_active is False
