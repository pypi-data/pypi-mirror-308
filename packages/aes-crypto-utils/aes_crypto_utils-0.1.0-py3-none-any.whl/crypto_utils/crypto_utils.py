# crypto_utils/crypto_utils.py

import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


def encrypt(password: str, secret_key: str) -> str:
    """
    Encrypts a password using AES encryption in ECB mode.
    
    Parameters:
        password (str): The plaintext password to encrypt.
        secret_key (str): The encryption key (must be 16, 24, or 32 bytes long).
    
    Returns:
        str: The encrypted password, encoded in base64.
    """
    key = secret_key.encode('utf-8')
    if len(key) not in (16, 24, 32):
        raise ValueError("Invalid secret_key length; must be 16, 24, or 32 bytes.")
    
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    
    pad_length = 16 - (len(password) % 16)
    padded_password = password + (chr(pad_length) * pad_length)
    
    encrypted = encryptor.update(padded_password.encode('utf-8')) + encryptor.finalize()
    return base64.b64encode(encrypted).decode('utf-8')


def unpad(data: bytes) -> bytes:
    """
    Unpads the decrypted data according to the padding scheme used in the encrypt function.
    
    Parameters:
        data (bytes): The decrypted data with padding.
    
    Returns:
        bytes: The unpadded data.
    """
    padding_length = data[-1]
    if padding_length < 1 or padding_length > 16:
        raise ValueError("Invalid padding detected.")
    return data[:-padding_length]


def decrypt(encrypted_text: str, secret_key: str) -> str:
    """
    Decrypts an AES-encrypted password in ECB mode.
    
    Parameters:
        encrypted_text (str): The base64-encoded encrypted password to decrypt.
        secret_key (str): The decryption key (must match the key used for encryption).
    
    Returns:
        str: The decrypted plaintext password.
    """
    key = secret_key.encode('utf-8')
    if len(key) not in (16, 24, 32):
        raise ValueError("Invalid secret_key length; must be 16, 24, or 32 bytes.")
    
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()
    
    decoded_data = base64.b64decode(encrypted_text)
    decrypted = decryptor.update(decoded_data) + decryptor.finalize()
    
    return unpad(decrypted).decode('utf-8')

