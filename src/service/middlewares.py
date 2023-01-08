from fastapi import Depends
from jose import JWSError, jwt
from models.exception_models import Unauthorized
from models.token_payload_model import TokenPayload
from service.auth_service import AuthService
from service.user_service import UserService

auth_service = AuthService()
user_service = UserService()

async def auth_middleware(token:str = Depends(auth_service.o_auth2_password_bearer)):
    try:
        payload = jwt.decode(token,key=auth_service.SECRET_KEY,algorithms=auth_service.ALGORITHM)
        token_payload = TokenPayload(**payload)
        return await user_service.get_user_by_id(int(token_payload.sub))
    except JWSError as jwt_err:
        print(jwt_err)
        raise Unauthorized()