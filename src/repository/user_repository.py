from models.user_models import UserDB
from repository.graph_database import GraphDatabase
from repository.sql_database import SqlDatabase


class UserRepository:
    def __init__(self):
        self.graph_database = GraphDatabase()
        self.sql_database = SqlDatabase()

    async def get_socialmedias_from_user(self,person_name:str):
        return await self.graph_database.get_socialmedias_from(person_name)

    async def get_all_connections_from_user(self,person_name:str, connection_type:str|None = None, social_media:str|None = None):
        return await self.graph_database.get_connections_from(person_name, connection_type, social_media)
    
    async def get_possible_connections(self,person_name:str, connection_type:str|None = None, social_media:str|None = None):
        return await self.graph_database.get_recommends_from(person_name, connection_type, social_media)

    async def get_influence_score(self,person_name:str,social_media:str):
        return await self.graph_database.get_influence_level_from(person_name, social_media)

    async def save_user(self, user:UserDB):
        self.sql_database.data[user.email] = user.__dict__

    async def get_user_by_email(self, email:str)->dict|None:
        try:
            return self.sql_database.data[email]
        except:
            return None
