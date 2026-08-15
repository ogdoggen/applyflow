from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def hash_password(password:str):
    return  password_hash.hash(password)


def verify_password(password:str, hashed_password:str):
    return hash_password(password) == hashed_password

