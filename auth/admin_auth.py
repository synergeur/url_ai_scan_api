
from pydantic import BaseModel
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

# Secret key for encoding and decoding JWT
SECRET_KEY = "your-secret-test"
ALGORITHM = "HS256"

# Pydantic model for token request body
class TokenData(BaseModel):
    token: str

# Generate a JWT token without an expiration time
def create_unlimited_access_token(data: dict):
    to_encode = data.copy()
    # No expiration time added to the payload
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Verify the token from the Authorization header
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")