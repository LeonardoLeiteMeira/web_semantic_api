from repository import Repository

# class to do some convertions and apply business logic on repository data
class Service:
    def __init__(self):
        self.repository = Repository()

    async def get_socialmedias_from_user(self, person_name:str):
            return await self.repository.get_socialmedias_from_user(person_name)

    async def get_all_connections_from_user(self, person_name:str, connection_type:str|None = None, social_media:str|None = None):
        return await self.repository.get_all_connections_from_user(person_name, connection_type, social_media)

    async def get_possible_connections(self, person_name:str, connection_type:str|None = None, social_media:str|None = None):
        return await self.repository.get_possible_connections(person_name,connection_type,social_media)

    async def get_influence_score(self,name:str,social_media:str,username_of_subgraph:str):
        return await self.repository.get_influence_score(name,social_media,username_of_subgraph)