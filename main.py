from typing import List
from services.auth_service.schemas import Login
from services.auth_service.service import Authentication
from pydantic import BaseModel
from fastapi import WebSocket


from services.user_service.schemas import UserProfileCreate
from services.user_service.service import UserService

from fastapi import UploadFile, File

# example to autentication with jwt
import redis
import uuid

# Endpoints to users

from fastapi import FastAPI, Depends, Response
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)

authentication_service = Authentication()


# password hashing
password = "minibumer12"
password_hashed = authentication_service.hash_password(password)
print(password_hashed)

# verify password
is_verified = authentication_service.verify_password("minibumer1", password_hashed)
print("IS VERIFIED", is_verified)


app = FastAPI()

authentication_service = Authentication()
user_service = UserService(auth_service=authentication_service)


# autenticacion con HTTPBearer
async def credentials(
    auth_credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
):
    token = auth_credentials.credentials
    payload = authentication_service.decode_payload(token)  # noqa

    return {
        "credentials": auth_credentials.credentials,
        "scheme": auth_credentials.scheme,
    }


# uso de OAuth2

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# crear una clase
class User(BaseModel):
    username: str
    email: str
    name: str


def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="example@example.com", name="josue"
    )


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


# TODO: review if login function is conflict with the other login function
@app.post("/login")
async def Login(form_data: Login, response: Response):
    user_found = user_service.get_user_by_email(form_data.email)

    session_id = str(uuid.uuid4())

    redis_connection = redis.Redis(host="localhost", port=6379, db=0)

    redis_connection.set(str(user_found["_id"]), session_id, ex=3600)

    if not user_found:
        return {"error": "User not found"}
    # validate the password
    if not authentication_service.verify_password(
        form_data.password, user_found["password"]
    ):
        return {"error": "Invalid credentials"}
    # pass more data
    token = authentication_service.encode_payload(
        str(user_found["_id"]), user_found["email"], user_found["username"]
    )
    response.set_cookie(key="cookie", value=token)
    return token

# pre register user
@app.post("/pre-register-user")
async def pre_register_user(user_data: UserPreCreate):
    ...

def validate_token(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    authentication_service.decode_payload(credentials.credentials)

# pre data collection
@app.get("/pre-data-collection")
async def pre_data_collection(data_collection: , ):

@app.post("/users")
async def create_user(user: UserProfileCreate):
    return user_service.register_user(user)


# test files


@app.post("/users/photo")
async def upload_user_photo(file: UploadFile = File(...)): ...


# Realtime

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
