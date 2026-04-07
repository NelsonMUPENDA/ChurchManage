"""
Custom DRF throttling classes for sensitive endpoints.
"""
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class LoginRateThrottle(AnonRateThrottle):
    """
    Throttle for login attempts.
    Limits: 5 attempts per minute per IP
    """
    scope = 'login'
    rate = '5/minute'


class RegisterRateThrottle(AnonRateThrottle):
    """
    Throttle for registration attempts.
    Limits: 3 attempts per hour per IP
    """
    scope = 'register'
    rate = '3/hour'


class SensitiveActionThrottle(UserRateThrottle):
    """
    Throttle for sensitive actions (financial transactions, user blocking, etc.)
    Limits: 10 actions per minute per user
    """
    scope = 'sensitive'
    rate = '10/minute'


class BurstRateThrottle(AnonRateThrottle):
    """
    Burst throttling for anonymous users.
    Limits: 20 requests per minute per IP
    """
    scope = 'anon'
    rate = '20/minute'


class SustainedRateThrottle(UserRateThrottle):
    """
    Sustained throttling for authenticated users.
    Limits: 100 requests per minute per user
    """
    scope = 'user'
    rate = '100/minute'
