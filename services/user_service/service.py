from pymongo import MongoClient

from services.user_service.schemas import UserProfileCreate

# establecer la conexion a la base de datos
# establecer el cliente
client = MongoClient("localhost", 27017)

# establecer la base de datos
data_base = client["realtime-chat"]

# getting a collection
collection = data_base["users"]


class UserRepository:
    ...


class UserService:

    def registe_user(self,user: UserProfileCreate):
        user_dict = user.model_dump()
        user_registered = collection.insert_one(user_dict)
        return {"user_id": str(user_registered.inserted_id)}

    def get_all_users(num: int, skip: int):
        ...

    def delete_users():
        ...