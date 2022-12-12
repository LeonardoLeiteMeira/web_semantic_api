from fastapi import APIRouter
from models.connection_model import ConnectionModel
from models.influence_score import InfluenceScore

from service import Service

router = APIRouter()
service = Service()

@router.get("/user/socialmedias/{name}", response_model=list[str])
async def get_social_medias(name:str):
    return await service.get_socialmedias_from_user(name)

@router.get("/user/connections/{name}",response_model=list[ConnectionModel])
async def get_user_connections(name:str, connection_type:str|None = None, social_media:str|None = None):
    return await service.get_all_connections_from_user(name,connection_type,social_media)

@router.get("/user/sugestion/{name}",response_model=list[ConnectionModel])
async def suggest_connections(name:str, connection_type:str|None = None, social_media:str|None = None):
    return await service.get_possible_connections(name,connection_type,social_media)

@router.get("/user/influence_score/{name}",response_model=InfluenceScore)
async def get_user_influence_score(name:str, social_media:str|None = None):
    return await service.get_influence_score(name,social_media)