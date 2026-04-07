"""
Custom password validators for stronger security.
"""
import re
from difflib import SequenceMatcher

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class MinimumLengthValidator:
    """
    Validate that the password is at least a minimum length.
    Default: 10 characters
    """

    def __init__(self, min_length=10):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                _(
                    "This password must contain at least %(min_length)d characters."
                ),
                code='password_too_short',
                params={'min_length': self.min_length},
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least %(min_length)d characters."
        ) % {'min_length': self.min_length}


class ComplexityValidator:
    """
    Validate that the password meets complexity requirements.
    Requires at least 3 of 4 character types:
    - Uppercase letters
    - Lowercase letters
    - Numbers
    - Special characters
    """

    def __init__(self, min_types=3):
        self.min_types = min_types

    def validate(self, password, user=None):
        char_types = 0
        
        if re.search(r'[A-Z]', password):
            char_types += 1
        if re.search(r'[a-z]', password):
            char_types += 1
        if re.search(r'\d', password):
            char_types += 1
        if re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]', password):
            char_types += 1
        
        if char_types < self.min_types:
            raise ValidationError(
                _(
                    "Your password must contain at least %(min_types)d of the following: "
                    "uppercase letters, lowercase letters, numbers, and special characters."
                ),
                code='password_not_complex',
                params={'min_types': self.min_types},
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least %(min_types)d of: uppercase letters, "
            "lowercase letters, numbers, and special characters."
        ) % {'min_types': self.min_types}


class CommonPasswordValidator:
    """
    Validate that the password is not a commonly used password.
    """

    # List of common weak passwords
    COMMON_PASSWORDS = {
        'password', '123456', '12345678', 'qwerty', 'abc123',
        'monkey', 'letmein', 'dragon', '111111', 'baseball',
        'iloveyou', 'trustno1', 'sunshine', 'princess', 'admin',
        'welcome', 'shadow', 'ashley', 'football', 'jesus',
        'michael', 'ninja', 'mustang', 'password1', '123456789',
        'adobe123', 'admin123', 'letmein1', 'photoshop', '1234567',
        'master', 'hello', 'freedom', 'whatever', 'qazwsx',
        'trustno1', '654321', 'jordan', 'harley', 'password123',
        'password12', 'password!', 'passw0rd', 'p@ssword',
    }

    def validate(self, password, user=None):
        if password.lower() in self.COMMON_PASSWORDS:
            raise ValidationError(
                _("This password is too common."),
                code='password_too_common',
            )

    def get_help_text(self):
        return _("Your password can't be a commonly used password.")


class UserAttributeSimilarityValidator:
    """
    Validate that the password is not too similar to user attributes.
    Checks: username, first_name, last_name, email
    """

    def __init__(self, max_similarity=0.7):
        self.max_similarity = max_similarity

    def validate(self, password, user=None):
        if not user:
            return

        attribute_values = [
            getattr(user, 'username', ''),
            getattr(user, 'first_name', ''),
            getattr(user, 'last_name', ''),
            getattr(user, 'email', ''),
        ]

        for value in attribute_values:
            if not value:
                continue
            
            # Check similarity
            similarity = SequenceMatcher(a=password.lower(), b=value.lower()).ratio()
            if similarity >= self.max_similarity:
                raise ValidationError(
                    _(
                        "The password is too similar to your personal information "
                        "(username, email, name)."
                    ),
                    code='password_too_similar',
                )

    def get_help_text(self):
        return _(
            "Your password can't be too similar to your other personal information "
            "like your username or email."
        )


class NoSequentialCharactersValidator:
    """
    Validate that the password doesn't contain sequential characters.
    Prevents passwords like '123456', 'abcdef', 'qwerty'
    """

    SEQUENCES = [
        'abcdefghijklmnopqrstuvwxyz',
        'zyxwvutsrqponmlkjihgfedcba',
        '0123456789',
        '9876543210',
        'qwertyuiop',
        'asdfghjkl',
        'zxcvbnm',
    ]

    def __init__(self, min_sequence_length=4):
        self.min_sequence_length = min_sequence_length

    def validate(self, password, user=None):
        password_lower = password.lower()
        
        for sequence in self.SEQUENCES:
            for i in range(len(sequence) - self.min_sequence_length + 1):
                seq = sequence[i:i + self.min_sequence_length]
                if seq in password_lower:
                    raise ValidationError(
                        _(
                            "Your password contains sequential characters (like '1234' or 'abcd'). "
                            "Please use a more random password."
                        ),
                        code='password_sequential',
                    )

    def get_help_text(self):
        return _(
            "Your password can't contain sequential characters (like '1234' or 'abcd')."
        )


class NoRepeatedCharactersValidator:
    """
    Validate that the password doesn't have too many repeated characters.
    """

    def __init__(self, max_repeats=3):
        self.max_repeats = max_repeats

    def validate(self, password, user=None):
        # Check for repeated characters like 'aaa', '1111'
        for i in range(len(password) - self.max_repeats):
            chunk = password[i:i + self.max_repeats + 1]
            if len(set(chunk)) == 1:  # All characters the same
                raise ValidationError(
                    _(
                        "Your password contains too many repeated characters. "
                        "Avoid using the same character more than %(max_repeats)d times in a row."
                    ),
                    code='password_repeated',
                    params={'max_repeats': self.max_repeats},
                )

    def get_help_text(self):
        return _(
            "Your password can't have more than %(max_repeats)d repeated characters in a row."
        ) % {'max_repeats': self.max_repeats}
