from fastapi import APIRouter, Query, Form, File, UploadFile, Cookie, HTTPException
from backend.src.MongoDB.mongoDB_client import mongoDB_client
from typing import Optional, Annotated
import base64
import json

router = APIRouter()

class NotAuthorizedError(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail="Not Authorized")

@router.post('/api/posts')
async def insert_post(
    title: Annotated[str, Query(max_length=255), Form()],
    description: Annotated[str, Form()],
    tag: Annotated[str, Query(max_length=255), Form()],
    image: UploadFile = File(...),
    session: Annotated[Optional[str], Cookie()] = None
):
    if session is None:
        raise NotAuthorizedError()
    
    try:
        user_info = json.loads(session)
        userId = user_info["userId"]
        postData={"title":title, "description": description, "tag": tag, "userId": userId}
        post= await mongoDB_client.insert_post(postData, image)
        
    except (KeyError, ValueError, base64.binascii.Error):
        raise HTTPException(status_code=400, detail="Invalid session token")
    
    return {"post": post}

    # # TODO: Save the post to the database
    # # You would add your database interaction here.
    # # Example (pseudo-code):
    # # new_post = {
    # #     "title": title,
    # #     "description": description,
    # #     "tags": tags.split(','),  # if tags are comma-separated
    # #     "image": image.filename if image else None,
    # #     "user_id": userId
    # # }
    # # result = await posts_collection.insert_one(new_post)

    # return {"userId": userId, "title": title, "description": description, "tags": tags}
