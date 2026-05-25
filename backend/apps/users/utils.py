"""
Utility functions for users app.
"""

import secrets
from django.utils import timezone
from datetime import timedelta
from .models import PasswordResetToken, EmailVerificationToken


def generate_password_reset_token(user, expires_in_hours=1):
    """
    Generate a password reset token for a user.
    
    Args:
        user: The user object
        expires_in_hours: Token expiration time in hours
    
    Returns:
        PasswordResetToken object
    """
    token = secrets.token_urlsafe(32)
    
    # Delete old tokens
    PasswordResetToken.objects.filter(user=user, is_used=False).delete()
    
    reset_token = PasswordResetToken.objects.create(
        user=user,
        token=token,
        expires_at=timezone.now() + timedelta(hours=expires_in_hours)
    )
    
    return reset_token


def generate_email_verification_token(user, expires_in_hours=24):
    """
    Generate an email verification token for a user.
    
    Args:
        user: The user object
        expires_in_hours: Token expiration time in hours
    
    Returns:
        EmailVerificationToken object
    """
    token = secrets.token_urlsafe(32)
    
    # Delete old tokens
    EmailVerificationToken.objects.filter(user=user, is_used=False).delete()
    
    verification_token = EmailVerificationToken.objects.create(
        user=user,
        token=token,
        expires_at=timezone.now() + timedelta(hours=expires_in_hours)
    )
    
    return verification_token


def validate_password_reset_token(token):
    """
    Validate a password reset token.
    
    Args:
        token: The token string
    
    Returns:
        Tuple (is_valid, token_object, error_message)
    """
    try:
        token_obj = PasswordResetToken.objects.get(token=token)
        
        if not token_obj.is_valid():
            return False, None, "Token is invalid or expired."
        
        return True, token_obj, None
    except PasswordResetToken.DoesNotExist:
        return False, None, "Token not found."


def validate_email_verification_token(token):
    """
    Validate an email verification token.
    
    Args:
        token: The token string
    
    Returns:
        Tuple (is_valid, token_object, error_message)
    """
    try:
        token_obj = EmailVerificationToken.objects.get(token=token)
        
        if not token_obj.is_valid():
            return False, None, "Token is invalid or expired."
        
        return True, token_obj, None
    except EmailVerificationToken.DoesNotExist:
        return False, None, "Token not found."
