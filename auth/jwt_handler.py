
import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_EXPIRATION_TIME = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))




def create_access_token(data:dict):
    to_encode = data.copy()
    
    expire = datetime.now() + timedelta(minutes=ACCESS_EXPIRATION_TIME)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
         