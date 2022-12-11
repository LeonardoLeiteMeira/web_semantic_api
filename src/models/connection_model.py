from pydantic import BaseModel


class ConnectionModel(BaseModel):
    name:str
    social_media:str
    username:str