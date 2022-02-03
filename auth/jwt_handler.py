# this file is responsible for signing , encoding , decoding and returning jwts

import time 
import jwt
from decouple import config

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")

# function return return generated token (JWT)
def token_response(token : str):
    return {
        "access token" : token
    }

# function is used for signing the jwt string
def signJWT(userID : str):
    payload = {
        "userID" : userID,
        "expiry" : time.time() + 600
    }

    token = jwt.encode(payload , JWT_SECRET , algorithm=JWT_ALGORITHM)
    return token_response(token)


# this function is used to decode the token
def decodeJWT(token : str):
    try:
        decode_token = jwt.decode(token , JWT_SECRET , algorithms=JWT_ALGORITHM)
        if decode_token["expiry"] >= time.time() :
            return decode_token
        else:
            return None
    except:
        return None