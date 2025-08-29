# encrypt.py
from Crypto.Cipher import AES
import base64
import sys

# -------------------------------
# Configuration
# -------------------------------
KEY = b"1234567890123456"  # 16-byte key (must be 16/24/32 for AES)
BLOCK_SIZE = 16            # AES block size

# -------------------------------

# PKCS7 Padding function
# -------------------------------
def pad(s):
    padding_len = BLOCK_SIZE - len(s) % BLOCK_SIZE
    return s + (chr(padding_len) * padding_len)

# -------------------------------
# Encrypt Function
# -------------------------------
def encrypt_password(password: str) -> str:
    cipher = AES.new(KEY, AES.MODE_ECB)
    padded = pad(password)
    encrypted_bytes = cipher.encrypt(padded.encode("utf-8"))
    return base64.b64encode(encrypted_bytes).decode("utf-8")

# -------------------------------
# Main
# -------------------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python encrypt.py welcome")
        sys.exit(1)

    password = sys.argv[1]
    encrypted = encrypt_password("welcome")
    print("hello ::",encrypted)