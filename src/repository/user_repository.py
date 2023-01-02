# from database import Database

from repository.database import Database


class UserRepository:
    def __init__(self):
        self.database = Database()

    async def get_socialmedias_from_user(self,person_name:str):
        return await self.database.get_socialmedias_from(person_name)

    async def get_all_connections_from_user(self,person_name:str, connection_type:str|None = None, social_media:str|None = None):
        return await self.database.get_connections_from(person_name, connection_type, social_media)
    
    async def get_possible_connections(self,person_name:str, connection_type:str|None = None, social_media:str|None = None):
        return await self.database.get_recommends_from(person_name, connection_type, social_media)

    async def get_influence_score(self,person_name:str,social_media:str):
        return await self.database.get_influence_level_from(person_name, social_media)

