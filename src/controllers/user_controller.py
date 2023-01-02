from fastapi import APIRouter

from service.user_service import UserService
from models.connection_model import ConnectionModel
from models.influence_score import InfluenceScore 

user_router = APIRouter()

userService = UserService()

@user_router.post("/create/")
async def create_new_user():
    return {"status": "Not Implemented"}

@user_router.get("/socialmedias/{id}", response_model=list[str])
async def get_social_medias(id:str):
    return await userService.get_socialmedias_from_user(id)

@user_router.get("/connections/{id}",response_model=list[ConnectionModel])
async def get_user_connections(id:str, connection_type:str|None = None, social_media:str|None = None):
    return await userService.get_all_connections_from_user(id,connection_type,social_media)

@user_router.get("/sugestion/{id}",response_model=list[ConnectionModel])
async def suggest_connections(id:str, connection_type:str|None = None, social_media:str|None = None):
    return await userService.get_possible_connections(id,connection_type,social_media)

@user_router.get("/influence_score/{id}",response_model=InfluenceScore)
async def get_user_influence_score(id:str, social_media:str|None = None):
    return await userService.get_influence_score(id,social_media)
