import jwt
from ..user.schemas import GetUserSchema
from fastapi import status, HTTPException


KEY = 'e8a9eee4-5305-442e-91a5-9f8fc4f67ed4'

# Encode (Create) a JWT
def encode_jwt(payload):
    token = jwt.encode(payload, KEY, algorithm='HS256')
    return token

# Decode (Verify) a JWT
def decode_jwt(token):
    try:
        payload = jwt.decode(token, KEY, algorithms=['HS256'])
        
        user_schema = GetUserSchema(**payload)
        
        if user_schema.cpf is None or user_schema.username is None or user_schema.email is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
        
        return user_schema
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
