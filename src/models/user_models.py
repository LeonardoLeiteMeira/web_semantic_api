from pydantic import BaseModel


class User(BaseModel):
    id:int|None
    email: str
    name: str
    disabled: bool|None = False

class CreateUser(User):
    password:str

class UserAuth(User):
    token:str
    token_type:str

class UserDB(User):
    hashed_password:str