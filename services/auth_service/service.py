import jwt
import os
from passlib.hash import bcrypt
from dataclasses import dataclass
from fastapi.exceptions import HTTPException 
from datetime import datetime, timezone, timedelta


secret_key = os.getenv("SECRET_KEY")
@dataclass
class Authentication:

    def encode_payload(self, user_id: str, email: str, username: str):
        # añadir los tipos de claims (payload) 
        payload = {"sub": user_id, "user_data": {"email": email, "name": username}, "exp": datetime.now(timezone.utc) + timedelta(minutes=1)}
        encoded = jwt.encode(payload, key=secret_key, algorithm="HS256")
        return encoded
    
    def decode_payload(self, access_token: str):
        try:
            data = jwt.decode(access_token,key=secret_key, algorithms="HS256")        
            return data
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    def hash_password(self, password: str):
        password_hashed = bcrypt.hash(password)
        return password_hashed
    
    def verify_password(self, current_password: str, hash_password: str):
        return bcrypt.verify(current_password, hash_password)
    
