from fastapi import APIRouter

router = APIRouter()

@router.get("/user/socialmedias/{name}")
async def root(name:str):
    return {
        "Description":"List socialmedias",
        "Name":name
    }

@router.get("/user/connections/{name}")
async def root(name:str, connection_type:str|None = None, social_media:str|None = None):
    return {
        "Description":"List connections",
        "name":name,
        "connection_type": connection_type,
        "social_media":social_media
    }

@router.get("/user/sugestion/{name}")
async def root(name:str, connection_type:str|None = None, social_media:str|None = None):
    return {
        "Description":"List sugestions",
        "name":name,
        "connection_type": connection_type,
        "social_media":social_media
    }

@router.get("/user/influence_score/{name}")
async def root(name:str, social_media:str|None = None, username_of_subgraph:str|None = None):
    return {
        "Description":"Gest Influence score",
        "name":name,
        "social_media":social_media,
        "username_of_subgraph": username_of_subgraph
    }