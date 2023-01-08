from models.user_models import UserDB
from repository.graph_database import GraphDatabase
from repository.sql_database import SqlDatabase
import random

class UserRepository:
    def __init__(self):
        self.graph_database = GraphDatabase()
        self.sql_database = SqlDatabase()

    async def get_socialmedias_from_user(self,user_id:int):
        return await self.graph_database.get_socialmedias_from(user_id)

    async def get_all_connections_from_user(self,user_id:int, type:str|None = None,):
        return await self.graph_database.get_connections_from(user_id, type)
    
    async def get_possible_connections(self,person_name:str, connection_type:str|None = None, social_media:str|None = None):
        return await self.graph_database.get_recommends_from(person_name, connection_type, social_media)

    async def get_influence_score(self,user_id:int):
        return await self.graph_database.get_influence_level_from(user_id)

    async def save_user(self, user:UserDB):
        user.id = random.randint(0,900)
        self.sql_database.data[user.id] = user.__dict__

    async def get_user_by_id(self, id:int)->dict|None:
        try:
            return self.sql_database.data[id]
        except:
            return None

    async def get_user_by_email(self, email:str)->dict|None:
        try:
            data = self.sql_database.data
            keys = data.keys()
            for key in keys:
                user = data[key]
                if user["email"] == email:
                    return user
        except:
            return None
