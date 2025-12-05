from cryptography.fernet import Fernet

def decrypt_string(encrypted_message: str, key: str) -> str:
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message.encode())
    return decrypted_message.decode()