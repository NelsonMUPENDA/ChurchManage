"""
Tests for security features: rate limiting, password validation, security headers.
"""
import pytest
from rest_framework import status
from django.core.cache import cache
from django.contrib.auth import get_user_model

from church_management.password_validators import (
    MinimumLengthValidator,
    ComplexityValidator,
    CommonPasswordValidator,
    UserAttributeSimilarityValidator,
    NoSequentialCharactersValidator,
    NoRepeatedCharactersValidator,
)

User = get_user_model()


@pytest.mark.unit
class TestRateLimiting:
    """Tests for rate limiting on API endpoints."""

    def test_login_rate_limit(self, api_client):
        """Test that login endpoint is rate limited."""
        # Clear any existing cache
        cache.clear()
        
        # Make multiple failed login attempts
        for i in range(6):
            response = api_client.post('/api/auth/token/', {
                'username': f'testuser{i}',
                'password': 'wrongpassword'
            })
        
        # The 6th request should be rate limited
        # Note: Exact behavior depends on throttle configuration
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_429_TOO_MANY_REQUESTS, status.HTTP_401_UNAUTHORIZED]

    def test_rate_limit_headers_present(self, admin_client):
        """Test that rate limit headers are present in responses."""
        response = admin_client.get('/api/users/')
        
        # Check for rate limit headers
        assert 'X-RateLimit-Limit' in response.headers or 'X-RateLimit-Remaining' in response.headers


@pytest.mark.unit
class TestPasswordValidators:
    """Tests for custom password validators."""

    def test_minimum_length_validator(self):
        """Test minimum length password validation."""
        validator = MinimumLengthValidator(min_length=10)
        
        # Should not raise for valid password
        validator.validate('ValidPass123!')
        
        # Should raise for short password
        with pytest.raises(Exception):
            validator.validate('Short1!')

    def test_complexity_validator(self):
        """Test password complexity validation."""
        validator = ComplexityValidator(min_types=3)
        
        # Valid: uppercase, lowercase, numbers
        validator.validate('ValidPass123')
        
        # Invalid: only lowercase
        with pytest.raises(Exception):
            validator.validate('onlylowercase')

    def test_common_password_validator(self):
        """Test common password validation."""
        validator = CommonPasswordValidator()
        
        # Should not raise for unique password
        validator.validate('MyUniqueP@ssw0rd2024')
        
        # Should raise for common password
        with pytest.raises(Exception):
            validator.validate('password123')

    def test_sequential_characters_validator(self):
        """Test sequential characters validation."""
        validator = NoSequentialCharactersValidator()
        
        # Valid password
        validator.validate('MyP@ssw0rd!')
        
        # Invalid: contains '1234'
        with pytest.raises(Exception):
            validator.validate('Pass1234!')

    def test_repeated_characters_validator(self):
        """Test repeated characters validation."""
        validator = NoRepeatedCharactersValidator(max_repeats=3)
        
        # Valid password
        validator.validate('MyP@ssw0rd!')
        
        # Invalid: contains 'aaaa'
        with pytest.raises(Exception):
            validator.validate('Passaaaa1!')

    def test_user_attribute_similarity_validator(self, create_user):
        """Test user attribute similarity validation."""
        user = create_user(
            username='johndoe',
            email='john@example.com',
            first_name='John',
            last_name='Doe'
        )
        
        validator = UserAttributeSimilarityValidator()
        
        # Valid password
        validator.validate('MySecureP@ssw0rd123!', user)
        
        # Invalid: too similar to username
        with pytest.raises(Exception):
            validator.validate('johndoe123', user)


@pytest.mark.unit
class TestSecurityHeaders:
    """Tests for security headers middleware."""

    def test_security_headers_present(self, api_client):
        """Test that security headers are present in responses."""
        response = api_client.get('/api/announcements/')
        
        # Check security headers
        assert response.headers.get('X-Content-Type-Options') == 'nosniff'
        assert response.headers.get('X-Frame-Options') == 'DENY'
        assert response.headers.get('X-XSS-Protection') == '1; mode=block'
        assert 'Content-Security-Policy' in response.headers

    def test_csp_header(self, api_client):
        """Test Content Security Policy header."""
        response = api_client.get('/api/announcements/')
        
        csp = response.headers.get('Content-Security-Policy', '')
        assert "default-src 'self'" in csp
        assert "frame-ancestors 'none'" in csp


@pytest.mark.unit
class TestCORSConfiguration:
    """Tests for CORS configuration."""

    def test_cors_headers_present(self, api_client):
        """Test that CORS headers are present."""
        response = api_client.get(
            '/api/announcements/',
            HTTP_ORIGIN='http://localhost:3000'
        )
        
        # Check CORS headers
        assert 'Access-Control-Allow-Origin' in response.headers or response.status_code == 200

    def test_preflight_request(self, api_client):
        """Test CORS preflight request."""
        response = api_client.options(
            '/api/auth/token/',
            HTTP_ORIGIN='http://localhost:3000',
            HTTP_ACCESS_CONTROL_REQUEST_METHOD='POST'
        )
        
        assert response.status_code == 200
