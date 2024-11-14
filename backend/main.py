from fastapi.exceptions import RequestValidationError
from backend.src.errors.custom_error import CustomError
from backend.src.middlewares.request_validation_handler import request_validation_error
from backend.src.middlewares.error_handler import error_handler
from backend.src.routes import user_routes
from backend.src.routes import post_routes
from backend.src.MongoDB.mongoDB_client import mongoDB_client
import os
from dotenv import load_dotenv

from fastapi import FastAPI

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    load_dotenv()
    if not os.getenv("MONGO_URI"):
        raise Exception("MONGO_URI not defined")
    if not os.getenv("JWT_KEY"):
        raise Exception("JWT_KEY not defined")
    await mongoDB_client.connect()
    
@app.on_event("shutdown")
async def shutdown():
    await mongoDB_client.close()


app.include_router(user_routes.router)
app.include_router(post_routes.router)

app.add_exception_handler(RequestValidationError, request_validation_error)
app.add_exception_handler(CustomError, error_handler) 