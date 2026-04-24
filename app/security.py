from passlib.context import CryptContext
import hashlib

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    prehashed = hashlib.sha256(password.encode()).hexdigest()
    return pwd_context.hash(prehashed)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    prehashed = hashlib.sha256(plain_password.encode()).hexdigest()
    return pwd_context.verify(prehashed, hashed_password)