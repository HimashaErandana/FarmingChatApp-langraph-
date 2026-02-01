from datetime import datetime,timedelta
from jose import jwt,JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from config import SECRET_KEY
import bcrypt
from db import DB

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30




#pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_pw(password:str):
    password_bytes = password.encode('utf-8')
    
    # Generate salt and hash
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password_bytes, salt)
    
    # Return as string
    return hashed.decode('utf-8')


def verify_pw(password:str,hashed_pw:str):
        plain_bytes = password.encode('utf-8')
        hashed_bytes = hashed_pw.encode('utf-8')
        return bcrypt.checkpw(plain_bytes, hashed_bytes)
#token creatoon

def create_access_token(username:str):
  expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  payload = {
      "sub": username,
      "exp": expire
  }
  return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)

#token verification


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")




async def get_current_user(token: str = Depends(oauth2_scheme)):
    from services.User.UserServices import UserService
    userss = UserService()
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")

        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        
        user = await userss.getuser_by_email(email)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Token expired or invalid")