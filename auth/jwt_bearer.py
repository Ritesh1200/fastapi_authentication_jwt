# this is for checking the user is authorize of not 

from fastapi import Request , HTTPException
from fastapi.security import HTTPAuthorizationCredentials , HTTPBearer
from .jwt_handler import decodeJWT

class jwtBearer(HTTPBearer):

    def __init__(self , auto_Error : bool = True):
        super(jwtBearer , self).__init__(auto_error=auto_Error)


    async def __call__(self , request : Request):
        credentials : HTTPAuthorizationCredentials = await super(jwtBearer , self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403 , detail="Invalid or Expired Token! ")
            payload = decodeJWT(credentials.credentials)
            if not payload:
                raise HTTPException(status_code=403 , detail="Invalid or Expired Token! ")
            return payload
        else:
            raise HTTPException(status_code=403 , detail="Invalid or Expired token! ")
