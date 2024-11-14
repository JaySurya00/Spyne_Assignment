from backend.src.MongoDB.mongoDB_client import mongoDB_client

async def uploadImage(image):
    image_id= mongoDB_client.__fs(image, image.name)
    return image_id