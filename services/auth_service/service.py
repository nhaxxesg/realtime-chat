import jwt
import os
from passlib.hash import bcrypt

secret_key = os.getenv("SECRET_KEY")

class Authentication:
    def encode_payload(self, email: str, name: str):
        payload = {"email": email, "name": name}
        encoded = jwt.encode(payload, key=secret_key, algorithm="HS256")
        return encoded
    
    def decode_payload(self, access_token: str):
        data = jwt.decode(access_token,key=secret_key, algorithms="HS256")        
        return data
    
    def hash_password(self, password: str):
        password_hashed = bcrypt.hash(password)
        return password_hashed
    
    def verify_password(self, current_password: str, hash_password: str):
        return bcrypt.verify(current_password, hash_password)
    