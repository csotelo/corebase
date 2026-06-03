"""Celery tasks for async email sending."""

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from config.celery import app


@app.task
def send_email_verification(user_id: int, token: str):
    """Send email verification link asynchronously.

    Args:
        user_id: ID of the user to verify.
        token: Email verification token.
    """
    from apps.users.models import CustomUser

    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return

    frontend_url = getattr(settings, "FRONTEND_URL", "http://localhost:3000")
    verify_url = f"{frontend_url}/verify-email/?token={token}"

    context = {
        "user_email": user.email,
        "verify_url": verify_url,
        "frontend_url": frontend_url,
    }

    subject = "Verify your email address"
    text_body = render_to_string("emails/verify_email.txt", context)
    html_body = render_to_string("emails/verify_email.html", context)

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    email.attach_alternative(html_body, "text/html")
    email.send(fail_silently=False)


@app.task
def send_password_reset(user_id: int, token: str):
    """Send password reset link asynchronously.

    Args:
        user_id: ID of the user requesting password reset.
        token: Password reset token.
    """
    from apps.users.models import CustomUser

    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return

    frontend_url = getattr(settings, "FRONTEND_URL", "http://localhost:3000")
    reset_url = f"{frontend_url}/reset-password/?token={token}"

    context = {
        "user_email": user.email,
        "reset_url": reset_url,
        "frontend_url": frontend_url,
    }

    subject = "Reset your password"
    text_body = render_to_string("emails/password_reset.txt", context)
    html_body = render_to_string("emails/password_reset.html", context)

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    email.attach_alternative(html_body, "text/html")
    email.send(fail_silently=False)
