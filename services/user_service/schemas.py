from pydantic import BaseModel


class UserProfile(BaseModel):
    id: int
    username: str
    email: str
    password: str
    created_at: str
    updated_at: str


class Photo(BaseModel):
    name: str
    image_type: str


class UserProfileCreate(BaseModel):
    username: str
    email: str
    password: str
    photo: Photo | None = None

class UserProfilePreCreate(BaseModel):
    