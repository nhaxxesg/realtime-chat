from services.auth_service.service import Authentication
from pydantic import BaseModel

from services.user_service.schemas import UserProfileCreate
from services.user_service.service import UserService
# example to autentication with jwt

authentication_service = Authentication()

access_token = authentication_service.encode_payload("algo@example", "sapee")
print(access_token)

data = authentication_service.decode_payload(access_token)
print(data)

# password hashing
password = "minibumer12"
password_hashed = authentication_service.hash_password(password)
print(password_hashed)

# verify password
is_verified = authentication_service.verify_password("minibumer1", password_hashed)
print("IS VERIFIED", is_verified)


# Endpoints to users

from fastapi import FastAPI, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

# autenticacion con HTTPBearer
async def credentials(auth_credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    return {"credentials": auth_credentials.credentials, "scheme": auth_credentials.scheme}


@app.post("/register-user")
async def register_user(token=Depends(credentials)):
    print(token)

# uso de OAuth2

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# crear una clase
class User(BaseModel):
    username: str
    email: str
    name: str

def fake_decode_token(token):
    return User(username=token+"fakedecoded", email="example@example.com",name="josue")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    return user

# codigo de chat gpt
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return {"access_token": "token generated", "token_type": "bearer"}

@app.get("/users")
async def get_users(current_user: str = Depends(get_current_user)):
    return current_user

user_service = UserService()

@app.post("/users")
async def create_user(user: UserProfileCreate):
    return user_service.registe_user(user)



