from models.user_models import CreateUser, User, UserAuth, UserDB
from repository.user_repository import UserRepository
from service.auth_service import AuthService
from models.exception_models import IncorrectLogin

# class to do some convertions and apply business logic on repository data
class UserService:
    def __init__(self):
        self.repository = UserRepository()
        self.auth_service = AuthService()

    async def get_socialmedias_from_user(self, user_id:int):
        return await self.repository.get_socialmedias_from_user(user_id)

    async def get_all_connections_from_user(self, user_id:int, type:str|None = None):
        return await self.repository.get_all_connections_from_user(user_id, type)

    async def get_possible_connections(self, user_id:int):
        current_connections:list = await self.repository.get_all_connections_from_user(user_id)
        possible_sugestions:list = await self.repository.get_possible_connections(user_id)
        connection = [possible for possible in possible_sugestions if possible not in current_connections]
        return connection

    async def get_influence_score(self,user_id:int):
        return await self.repository.get_influence_score(user_id)

    async def create_user(self, new_user:CreateUser):
        hashed_password = self.auth_service.hash_password(new_user.password)
        user_db = UserDB(**new_user.__dict__,hashed_password=hashed_password)
        await self.repository.save_user(user_db)
        return await self.validate_login(new_user.email,new_user.password)

    async def get_user_by_id(self,user_id:int)-> User|None:
        try:
            user_dict = await self.repository.get_user_by_id(user_id)
            if user_dict:
                return User(**user_dict)
        except Exception as er:
            print(er)
            return None

    async def get_user_by_email(self, user_email:str):
        user_dict = await self.repository.get_user_by_email(user_email)
        if user_dict:
            user_db = UserDB(**user_dict)
            if not user_db.disabled:
                return user_db
            else:
                raise IncorrectLogin("User is diabled")
        else:
            raise IncorrectLogin()

    async def validate_login(self, user_email:str, password:str):
        user_db = await self.get_user_by_email(user_email)
        if self.auth_service.verify_password(password, user_db.hashed_password):
            token = self.auth_service.create_bearer_token(user_db.id,{})
            return UserAuth(**user_db.__dict__ ,token_type="bearer",access_token=token)
        else:
            raise IncorrectLogin()