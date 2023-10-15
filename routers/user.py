from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from utils.jwt_manager import create_token
from schemas.user import User

user_router = APIRouter()


#Authentification
@user_router.post("/login", tags=["auth"])
async def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token:str = create_token(user.dict())
        return JSONResponse(content=token, status_code=200)
    

@user_router.post("/login2", tags=["form"])
async def login2(user: str = Form(), password: str = Form()):
    return {"username": user, "password": password}