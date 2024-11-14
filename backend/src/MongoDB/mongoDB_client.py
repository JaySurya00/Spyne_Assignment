from pymongo import AsyncMongoClient,MongoClient
from typing import List, Optional
from backend.src.errors.database_connection_error import DatabaseConnectionError
import os
import gridfs


class MongoDB:
    __client: Optional[AsyncMongoClient] = None
    
    async def connect(self):
        if self.__client is not None:
            return self.__client
        try:
            self.__client = AsyncMongoClient(
                os.getenv("MONGO_URI")
            )
            self.__DB= self.__client['Spyne']
            self.__fs = gridfs.GridFS(database=MongoClient(os.getenv("MONGO_URI"))["Spyne"], collection='images')
            server_info = await self.__client.server_info()
            print(f"Connected to MongoDB: {server_info}")
        except Exception as ex:
            raise Exception(f"Cannot connect to MongoDB: {ex}")
        
    async def close(self):
        try:
            await self.__client.close()
        except Exception as e:
            raise DatabaseConnectionError()
        
    async def insert_user(self, user):
        try:
            users= self.__DB['users']
            userId= (await users.insert_one({"name": user.name, "email": user.email, "password": user.password})).inserted_id
            return {
                "id": str(userId),
                "name": user.name,
                "email":user.email
            }
        except Exception as e:
            raise DatabaseConnectionError()
        
    async def find_user(self, userData):
        try:
            users= self.__DB['users']
            user= (await users.find_one({"email": userData["email"], "password": userData["password"]}))
            if user is not None:
                return {"userId": str(user['_id']), "email": user['email']}
            return None
        except Exception as e:
            print(f'exception occured {e}')
            raise DatabaseConnectionError()
        
    async def insert_post(self, postData, image):
        try:
            posts= self.__DB['posts']
            title= postData["title"]
            description= postData["description"]
            tag= postData["tag"]
            image_id= self.__fs(image, filename=title)
            
            print(f"{title}, {description},{tag}, {image_id}")
            
            postId= (await posts.insert_one({"title": title, "description": description, "tag": tag, "imageId": image_id})).inserted_id
            
            return postId
            
        except Exception as e:
            print(f'exception occured {e}')
            raise DatabaseConnectionError()
        
        
        
            

mongoDB_client = MongoDB()
