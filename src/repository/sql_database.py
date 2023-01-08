from models.singleton import Singleton


class SqlDatabase(metaclass=Singleton):
    def __init__(self) -> None:
        self.data  = {
            1:{
                "id":1,
                "email":"leonardo@email.com",
                "name": "Leonardo Leite",
                "hashed_password":"leonardo123",
                "disabled": False
            },
            2:{
                "id":2,
                "email": "alice@email.com",
                "name":"Alice Leite Cazita",
                "hashed_password":"alice123",
                "disabled":True
            }

            
}
