from pydantic import BaseModel


class UserProfile(BaseModel):
    id: int
    username: str
    email: str
    password: str
    created_at: str
    updated_at: str

class UserProfileCreate(BaseModel):
    username: str
    email: str
    password: str