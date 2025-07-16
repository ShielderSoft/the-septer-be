from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from core.config import settings
from core.db import get_db
from models.user import User
import re

# ==================== JWT & ACCESS CONTROL ====================

# OAuth2 Bearer token setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def create_access_token(data: dict, expires_minutes: int = 60) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret, algorithm="HS256")
    return encoded_jwt

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise credentials_exception

    return user

def require_guardian(
    current_user: User = Depends(get_current_user)
) -> User:
    if current_user.role != "Guardian":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

def is_strong_password(password: str) -> bool:
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

# ==================== AES-256 ENCRYPTION ====================

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
import os
import binascii

# AES constants
KEY_LENGTH = 32  # 256 bits
PBKDF2_ITERATIONS = 100_000
IV_LENGTH = 16
backend = default_backend()

# Load secrets from environment
PASSPHRASE = settings.septer_aes_secret.encode()

# Get SALT from .env
try:
    SALT = binascii.unhexlify(settings.septer_aes_salt)  # 'this_is_salt'
except binascii.Error:
    raise ValueError("Invalid hex value for SEPTER_AES_SALT in .env")

# Get IV base from .env
try:
    IV_BASE = binascii.unhexlify(settings.septer_aes_iv_base)  # 'iv_base_char'
except binascii.Error:
    raise ValueError("Invalid hex value for SEPTER_AES_IV_BASE in .env")

# Derive AES-256 key from passphrase + salt
def _derive_key(passphrase: bytes, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_LENGTH,
        salt=salt,
        iterations=PBKDF2_ITERATIONS,
        backend=backend
    )
    return kdf.derive(passphrase)

AES_KEY = _derive_key(PASSPHRASE, SALT)

# Encrypt password (AES-256-CBC, PKCS7 padded, base64 encoded)
def encrypt_password(plaintext_password: str) -> str:
    iv = IV_BASE  # Fixed IV from .env
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext_password.encode()) + padder.finalize()
    cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(padded_data) + encryptor.finalize()
    return base64.b64encode(iv + encrypted).decode()

# Decrypt password
def decrypt_password(encrypted_password: str) -> str:
    encrypted_data = base64.b64decode(encrypted_password)
    iv = encrypted_data[:IV_LENGTH]
    ciphertext = encrypted_data[IV_LENGTH:]
    cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(iv), backend=backend)
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
    return plaintext.decode()

# Compare decrypted DB password with user-submitted plaintext
def verify_password(plain_password: str, encrypted_password: str) -> bool:
    try:
        return plain_password == decrypt_password(encrypted_password)
    except Exception:
        return False
