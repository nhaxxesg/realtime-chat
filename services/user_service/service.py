from pymongo import MongoClient
from datetime import datetime
from services.user_service.schemas import UserProfileCreate
from services.auth_service.service import Authentication

# establecer la conexion a la base de datos
# establecer el cliente
client = MongoClient("localhost", 27017)

# establecer la base de datos
data_base = client["realtime-chat"]

# getting a collection
collection = data_base["users"]


class UserRepository:
    ...


from dataclasses import dataclass
@dataclass
class UserService:
    auth_service: Authentication

    def register_user(self,user: UserProfileCreate):
        user_dict = user.model_dump()
        
        now_data = datetime.now()

        user_dict["password"] = self.auth_service.hash_password(user_dict["password"])

        user_dict["create_at"] = now_data
        user_dict["update_at"] = now_data

        print(user_dict)

        user_registered = collection.insert_one(user_dict)
        return {"user_id": str(user_registered.inserted_id)}

    def get_all_users(num: int, skip: int):
        ...

    def delete_users():
        ...

    def get_user_by_email(self, email: str):
        user_found = collection.find_one({"email": email})
        return user_found
    