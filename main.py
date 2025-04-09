from typing import List
from services.auth_service.schemas import Login
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

authentication_service = Authentication()
user_service = UserService(auth_service=authentication_service)

# autenticacion con HTTPBearer
async def credentials(auth_credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    token = auth_credentials.credentials
    payload = authentication_service.decode_payload(token)

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

@app.post("/login")
async def login(form_data: Login):
    user_found = user_service.get_user_by_email(form_data.email)
    if not user_found:
        return {"error": "User not found"}
    # validate the password
    if not authentication_service.verify_password(form_data.password, user_found["password"]):
        return {"error": "Invalid credentials"}
    return authentication_service.encode_payload(user_found["email"], user_found["username"])

def validate_token(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    authentication_service.decode_payload(credentials.credentials)

from fastapi import UploadFile, File

@app.post("/users")
async def create_user(user: UserProfileCreate, token: dict = Depends(validate_token), ):
    return user_service.register_user(user)

# test files

@app.post("/users/photo")
async def upload_user_photo(file: UploadFile = File(...)):
    ...

# Realtime
from fastapi import WebSocket

websockets_clients: List[WebSocket] = []

@app.websocket("/ws")
async def chat(websocket: WebSocket):
    await websocket.accept()
    print(websocket)
    websockets_clients.append(websocket)
    while True:
        message = await websocket.receive_text()
        await websocket.send_text(f"Mensaje enviado -> {message}")
        for client in websockets_clients:
            await websocket.send_text("Texto de websockets")