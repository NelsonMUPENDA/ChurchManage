"""
Tests for members API: Members, Families, HomeGroups, Departments, Ministries.
"""
import pytest
from rest_framework import status


@pytest.mark.unit
class TestMemberViewSet:
    """Tests for the /api/members/ endpoint."""

    def test_list_members_admin(self, admin_client, create_member):
        """Test that admins can list members."""
        create_member()
        response = admin_client.get('/api/members/')
        assert response.status_code == status.HTTP_200_OK

    def test_list_members_unauthorized(self, authenticated_client):
        """Test that regular users cannot list members."""
        response = authenticated_client.get('/api/members/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_member_admin(self, admin_client, create_user, create_family, create_home_group, create_department):
        """Test that admins can create members."""
        user = create_user(username='newmemberuser')
        family = create_family()
        home_group = create_home_group()
        department = create_department()

        data = {
            'user': user.id,
            'family': family.id,
            'home_group': home_group.id,
            'department': department.id,
            'gender': 'M'
        }
        response = admin_client.post('/api/members/', data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_search_members(self, admin_client, create_member):
        """Test member search functionality."""
        member = create_member()
        user = member.user
        user.first_name = 'John'
        user.save()

        response = admin_client.get('/api/members/?q=John')
        assert response.status_code == status.HTTP_200_OK

    def test_member_fiche_pdf(self, admin_client, create_member):
        """Test generating member PDF fiche."""
        member = create_member()
        response = admin_client.get(f'/api/members/{member.id}/fiche/')
        assert response.status_code == status.HTTP_200_OK
        assert response['Content-Type'] == 'application/pdf'


@pytest.mark.unit
class TestFamilyViewSet:
    """Tests for the /api/families/ endpoint."""

    def test_list_families_admin(self, admin_client, create_family):
        """Test that admins can list families."""
        create_family()
        response = admin_client.get('/api/families/')
        assert response.status_code == status.HTTP_200_OK

    def test_create_family_admin(self, admin_client):
        """Test that admins can create families."""
        data = {
            'name': 'New Family',
            'description': 'Family description'
        }
        response = admin_client.post('/api/families/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'New Family'


@pytest.mark.unit
class TestHomeGroupViewSet:
    """Tests for the /api/home-groups/ endpoint."""

    def test_list_home_groups_admin(self, admin_client, create_home_group):
        """Test that admins can list home groups."""
        create_home_group()
        response = admin_client.get('/api/home-groups/')
        assert response.status_code == status.HTTP_200_OK

    def test_create_home_group_admin(self, admin_client):
        """Test that admins can create home groups."""
        data = {
            'name': 'New Group',
        }
        response = admin_client.post('/api/home-groups/', data)
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.unit
class TestDepartmentViewSet:
    """Tests for the /api/departments/ endpoint."""

    def test_list_departments_admin(self, admin_client, create_department):
        """Test that admins can list departments."""
        create_department()
        response = admin_client.get('/api/departments/')
        assert response.status_code == status.HTTP_200_OK

    def test_create_department_admin(self, admin_client):
        """Test that admins can create departments."""
        data = {
            'name': 'New Department',
            'description': 'Department description'
        }
        response = admin_client.post('/api/departments/', data)
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.unit
class TestMinistryViewSet:
    """Tests for the /api/ministries/ endpoint."""

    def test_list_ministries_admin(self, admin_client):
        """Test that admins can list ministries."""
        from church_management.models import Ministry
        Ministry.objects.create(name='Test Ministry')
        response = admin_client.get('/api/ministries/')
        assert response.status_code == status.HTTP_200_OK

    def test_create_ministry_admin(self, admin_client):
        """Test that admins can create ministries."""
        data = {
            'name': 'New Ministry',
            'description': 'Ministry description'
        }
        response = admin_client.post('/api/ministries/', data)
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
class TestActivityDurationViewSet:
    """Tests for the /api/activity-durations/ endpoint."""

    def test_list_activity_durations_read_only(self, api_client):
        """Test that activity durations are publicly readable."""
        from church_management.models import ActivityDuration
        ActivityDuration.objects.create(label='Test Duration', code='test-dur')
        response = api_client.get('/api/activity-durations/')
        assert response.status_code == status.HTTP_200_OK

    def test_create_activity_duration_admin(self, admin_client):
        """Test that admins can create activity durations."""
        data = {
            'label': 'New Duration',
            'code': 'new-dur'
        }
        response = admin_client.post('/api/activity-durations/', data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_filter_activity_durations(self, admin_client):
        """Test filtering activity durations by is_active."""
        from church_management.models import ActivityDuration
        ActivityDuration.objects.create(label='Active', code='active-dur', is_active=True)
        ActivityDuration.objects.create(label='Inactive', code='inactive-dur', is_active=False)

        response = admin_client.get('/api/activity-durations/?is_active=true')
        assert response.status_code == status.HTTP_200_OK
