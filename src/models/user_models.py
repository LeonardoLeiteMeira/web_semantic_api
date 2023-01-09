from pydantic import BaseModel


class User(BaseModel):
    id:int|None
    email: str
    name: str
    disabled: bool|None = False

class CreateUser(BaseModel):
    email: str
    name: str
    password:str

class UserAuth(User):
    access_token:str
    token_type:str

class UserDB(User):
    hashed_password:str