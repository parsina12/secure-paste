from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from os import urandom
import base64

SECRET_KEY = b'your-32-byte-random-key--------'  # Change for production

def encrypt_text(plain_text: str) -> (str, str):
    iv = urandom(16)
    cipher = Cipher(algorithms.AES(SECRET_KEY), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ct = encryptor.update(plain_text.encode()) + encryptor.finalize()
    return base64.urlsafe_b64encode(iv).decode(), base64.urlsafe_b64encode(ct).decode()

def decrypt_text(iv_b64: str, ct_b64: str) -> str:
    iv = base64.urlsafe_b64decode(iv_b64)
    ct = base64.urlsafe_b64decode(ct_b64)
    cipher = Cipher(algorithms.AES(SECRET_KEY), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    return (decryptor.update(ct) + decryptor.finalize()).decode()
