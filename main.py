from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Any, Coroutine, Optional, List
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from utils.jwt_manager import create_token, validate_token
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from config.database import Session, engine, Base
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.error_handler import ErrorHandler
from middlewares.jwt_bearer import JWTBearer
from routers.movie import movie_router
from routers.user import user_router

app = FastAPI()
app.title = "Mi aplicación con FastAPI prueba"
app.description = "Aprendiendo FAST API Yupiiiiiii!"
app.version = "0.0.1"
#app.mount("/static", StaticFiles(directory="static"), name="static")



app.add_middleware(ErrorHandler)
app.include_router(movie_router)
app.include_router(user_router)

Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")


@app.get("/", tags=["home"])
async def message(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
 
#if __name__ == "__main__":
#       import uvicorn
#       uvicorn.run(app, host="127.0.0.1", port=8000)


    