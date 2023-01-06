from models.user_models import CreateUser, User, UserAuth, UserDB
from repository.user_repository import UserRepository
from service.auth_service import AuthService
from models.exception_models import IncorrectLogin

# class to do some convertions and apply business logic on repository data
class UserService:
    def __init__(self):
        self.repository = UserRepository()
        self.auth_service = AuthService()

    async def get_socialmedias_from_user(self, person_name:str):
        return await self.repository.get_socialmedias_from_user(person_name)

    async def get_all_connections_from_user(self, person_name:str, connection_type:str|None = None, social_media:str|None = None):
        return await self.repository.get_all_connections_from_user(person_name, connection_type, social_media)

    async def get_possible_connections(self, person_name:str, connection_type:str|None = None, social_media:str|None = None):
        return await self.repository.get_possible_connections(person_name,connection_type,social_media)

    async def get_influence_score(self,name:str,social_media:str):
        return await self.repository.get_influence_score(name,social_media)

    async def create_user(self, new_user:CreateUser):
        hashed_password = self.auth_service.hash_password(new_user.password)
        user_db = UserDB(**new_user.__dict__,hashed_password=hashed_password)
        await self.repository.save_user(user_db)
        return await self.validate_login(new_user.email,new_user.password)

    async def get_user_by_email(self,user_email:str)-> User|None:
        try:
            user_dict = await self.repository.get_user_by_email(user_email)
            if user_dict:
                return User(**user_dict)
        except Exception as er:
            print(er)
            return None

    async def service_get_user(self, user_email:str):
        user_dict = await self.repository.get_user_by_email(user_email)
        if user_dict:
            user_db = UserDB(**user_dict)
            if not user_db.disabled:
                return UserDB(**user_dict)
            else:
                raise IncorrectLogin("User is diabled")
        else:
            raise IncorrectLogin()

    async def validate_login(self, user_email:str, password:str):
        user_db = await self.service_get_user(user_email)
        if self.auth_service.verify_password(password, user_db.hashed_password):
            token = self.auth_service.create_bearer_token({"sub":user_db.email})
            return UserAuth(email=user_db.email,name=user_db.name,disabled=user_db.disabled,token=token, token_type="bearer")
        else:
            raise IncorrectLogin()