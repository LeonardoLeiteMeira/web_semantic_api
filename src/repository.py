from database.database import Database

#mocked data
class Repository:
    def __init__(self):
        self.database = Database()

    async def get_socialmedias_from_user(self,person_name:str):
        return ["Instagram","Youtube","Twitter"]

    async def get_all_connections_from_user(self,person_name:str, connection_type:str|None = None, social_media:str|None = None):
        return [
            {"name":"Alice", "social_media":"Instagram", "username":"Alice_Instagram"},
            {"name":"Cicero", "social_media":"Instagram", "username":"Cicero_Instagram"},
            {"name":"Laura", "social_media":"Youtube", "username":"Laura_Youtube"},
            {"name":"Artur", "social_media":"Tiktok", "username":"Artur_Tiktok"},
        ]

    async def get_possible_connections(self,person_name:str, connection_type:str|None = None, social_media:str|None = None):
        return [
            {"name":"Laura", "social_media":"Youtube", "username":"Laura_Youtube"},
            {"name":"Alice", "social_media":"Instagram", "username":"Alice_Instagram"},
        ]

    async def get_influence_score(self,person_name:str,social_media:str,username_of_subgraph:str):
        return {"user":person_name,"influence_score":10}

