from fastapi import APIRouter, Depends
from models.user_models import CreateUser, User
from service.middlewares import auth_middleware

from service.user_service import UserService
from models.connection_model import ConnectionModel
from models.influence_score import InfluenceScore 

user_router = APIRouter()

user_service = UserService()

@user_router.get("/socialmedias/{id}", response_model=list[str])
async def get_social_medias(id:str,user: User = Depends(auth_middleware)):
    return await user_service.get_socialmedias_from_user(id)

@user_router.get("/connections/{id}",response_model=list[ConnectionModel])
async def get_user_connections(id:int, type:str|None = None,user: User = Depends(auth_middleware)):
    return await user_service.get_all_connections_from_user(id,type)

@user_router.get("/sugestion/{id}",response_model=list[ConnectionModel])
async def suggest_connections(id:int,user: User = Depends(auth_middleware)):
    return await user_service.get_possible_connections(id)

@user_router.get("/influence_score/{id}",response_model=InfluenceScore,)
async def get_user_influence_score(id:int,user: User = Depends(auth_middleware)):
    return await user_service.get_influence_score(id)

@user_router.post("/signup")
async def create_user(new_user:CreateUser):
    return await user_service.create_user(new_user)

@user_router.get("/getuser")
async def get_test(user: User = Depends(auth_middleware)):
    user = await user_service.get_user_by_id(user.id)
    return user
