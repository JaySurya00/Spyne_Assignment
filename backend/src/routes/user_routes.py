from fastapi import APIRouter, HTTPException
from typing import Annotated
import json
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, constr

from backend.src.MongoDB.mongoDB_client import mongoDB_client
from backend.src.errors.bad_request_error import BadRequestError

router= APIRouter()

class User(BaseModel):
    name: constr(min_length=1)
    email: EmailStr
    password: constr(min_length=8)
    
class LoginRequest(BaseModel):
    email: str
    password: str
    
    
@router.post('/api/signup')
async def signup(user:User):
    existingUser= await mongoDB_client.find_user({"email": user.email, "password": user.password})
    if existingUser is not None:
        raise BadRequestError('User already exist')
        
    newUser= await mongoDB_client.insert_user(user)
        
    return newUser


@router.post('/api/login')
async def login(userData:LoginRequest):
    existingUser= await mongoDB_client.find_user({"email": userData.email, "password": userData.password})
        
    if existingUser is None:
        raise BadRequestError('Invalid email or password')
    
    user_data = json.dumps({"userId": existingUser["userId"], "email": existingUser["email"]})
    response = JSONResponse(content={"user": existingUser})
    response.set_cookie(key="session", value=user_data)
    return response

@router.post('/api/logout')
async def logout():
    response = JSONResponse(content={"message": "Logout successful"})
    
    # Set the cookie to expire in the past (this will delete it)
    response.set_cookie(key="session", value="")
    return response