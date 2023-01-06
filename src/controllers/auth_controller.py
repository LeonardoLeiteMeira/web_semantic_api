
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from models.user_models import CreateUser, User, UserAuth
from models.exception_models import IncorrectLogin
from service.auth_service import AuthService
from service.middlewares import auth_middleware
from service.user_service import UserService

auth_service = AuthService()
user_service = UserService()

auth_router = APIRouter()

@auth_router.post("/login", response_model=UserAuth)
async def login(form_data:OAuth2PasswordRequestForm = Depends()):
    try:
        user_authenticated = await user_service.validate_login(form_data.username, form_data.password)
        return user_authenticated
    except IncorrectLogin as e:
        message = "Incorrect username or password. "
        if len(e.args)>0:
            message += str(e.args[0])
        raise HTTPException(status_code=400,detail=message)
    except Exception as er:
        print(er)
        raise HTTPException(status_code=500, detail="Something Wrong here")