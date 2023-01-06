from models.singleton import Singleton


class SqlDatabase(metaclass=Singleton):
    def __init__(self) -> None:
        self.data  = {
            "leonardo@email.com":{
                "email":"leonardo@email.com",
                "name": "Leonardo Leite",
                "hashed_password":"leonardo123",
                "disabled": False
            },
            "alice@email.com":{
                "email": "alice@email.com",
                "name":"Alice Leite Cazita",
                "hashed_password":"alice123",
                "disabled":True
            }

            
}
