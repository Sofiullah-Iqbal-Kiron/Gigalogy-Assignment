from passlib.context import CryptContext


def send_confirmation_email(email: str):
    print(f"Sending confirmation email to {email}")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_raw_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
