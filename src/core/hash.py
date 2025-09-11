# 3'rd party
from passlib.context import CryptContext
from itsdangerous import URLSafeTimedSerializer

# local
from src.core.jwt import SECRET_KEY


pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")
serializer = URLSafeTimedSerializer(SECRET_KEY)
SALT = "email-verification-salt"


def hash_raw_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def sign_email(email: str) -> str:
    return serializer.dumps(email, salt=SALT)


def decode_signed_email(token: str, expiration=3600) -> str | None:
    try:
        email = serializer.loads(token, salt=SALT, max_age=expiration)
    except Exception:
        return None
    return email
