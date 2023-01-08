from pydantic import BaseModel


class ConnectionModel(BaseModel):
    id:int
    social_media:str
    email:str
