from pwdlib import PasswordHash
from jwt import decode, ExpiredSignatureError, InvalidTokenError
from auth.jwt_handler import SECRET_KEY, ALGORITHM

password_hash = PasswordHash.recommended()

def get_password_hash(password: str):
    return password_hash.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return password_hash.verify(plain_password, hashed_password)




def verify_access_token(token: str):
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        return None  
    except InvalidTokenError:
        return None  