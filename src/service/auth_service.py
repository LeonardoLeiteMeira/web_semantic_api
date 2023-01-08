from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt


class AuthService:
    def __init__(self):
        self.SECRET_KEY = "85dd92549a580674063fa6c9ebc98e34c09a2c2916c84cd3f9aa09aed1d5b8df"
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 30
        self.o_auth2_password_bearer = OAuth2PasswordBearer(tokenUrl="/auth/login")
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self,plain_text_password:str, hashed_password:str):
        return self.pwd_context.verify(plain_text_password,hashed_password)

    def hash_password(self,password:str):
        return self.pwd_context.hash(password)

    def create_bearer_token(self,user_id:int, data:dict):
        data_to_enconde = data.copy()
        expire = datetime.now()+timedelta(hours=1)
        data_to_enconde["exp"] = expire
        data_to_enconde["sub"] = str(user_id)
        return jwt.encode(claims=data_to_enconde,key=self.SECRET_KEY,algorithm=self.ALGORITHM)
