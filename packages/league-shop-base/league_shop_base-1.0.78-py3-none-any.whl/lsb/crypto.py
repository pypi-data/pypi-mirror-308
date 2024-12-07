from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
from django.conf import settings


def encode(data: str):
    return bytes(data, "raw_unicode_escape")


def decode(data: bytes):
    return str(data, "raw_unicode_escape")


def encrypt(value: str):
    return decode(f.encrypt(encode(value)))


def decrypt(value: str):
    try:
        return decode(f.decrypt(encode(value)))
    except InvalidToken:
        return "Invalid Token"


def decrypt_by_key(value: str, key: str):
    try:
        f = Fernet(encode(key))
        return decode(f.decrypt(encode(value)))
    except InvalidToken:
        return "Invalid Token"


def is_encrypted(value: str):
    return value.startswith("gAAAAA")


if hasattr(settings, "ENCRYPTION_KEY"):
    f = Fernet(encode(settings.ENCRYPTION_KEY))
