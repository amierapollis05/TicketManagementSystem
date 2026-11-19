from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

from flask import current_app

TOKEN_SALT = "supportdesk-resolution-review-v1"
TOKEN_MAX_AGE = 60 * 60 * 24 * 7  # 7 days


def generate_resolution_token(
    resolution_id: int,
    incident_id: int,
    user_id: int,
) -> str:
    """Generate a signed, time-limited resolution review token."""

    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])

    return serializer.dumps(
        {
            "resolution_id": resolution_id,
            "incident_id": incident_id,
            "user_id": user_id,
        },
        salt=TOKEN_SALT,
    )


def verify_resolution_token(token: str):
    """Verify a resolution token and return its signed payload."""

    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])

    try:
        payload = serializer.loads(
            token,
            salt=TOKEN_SALT,
            max_age=TOKEN_MAX_AGE,
        )

    except (BadSignature, SignatureExpired):
        return None

    if not isinstance(payload, dict):
        return None

    required_fields = ("resolution_id", "incident_id", "user_id")

    if any(
        not isinstance(payload.get(field), int) or payload[field] <= 0
        for field in required_fields
    ):
        return None

    return payload
