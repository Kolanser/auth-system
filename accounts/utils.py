import jwt
from datetime import timedelta
from django.conf import settings
from django.utils import timezone


def generate_jwt(user):
    expires_at = timezone.now() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_LIFETIME_MINUTES)
    payload = {
        "user_id": user.id,
        "iat": int(timezone.now().timestamp()),
        "exp": int(expires_at.timestamp()),
    }
    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        "HS256",
    )
    return token
