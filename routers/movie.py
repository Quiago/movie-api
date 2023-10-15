from fastapi import APIRouter
from fastapi import Path, Query, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()


@movie_router.get("/movies", tags=["movies"], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
async def get_movies() -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies()
    return JSONResponse(content=jsonable_encoder(result), status_code=200)

@movie_router.get("/movies/{id}", tags=["movies"], response_model=Movie,status_code=200)
async def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    #for item in movies:
    #    if item["id"] == id:
    #        return JSONResponse(content=item,status_code=200)

    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={"message": "No encontrado"})
    return JSONResponse(content=jsonable_encoder(result), status_code=200)

@movie_router.get("/movies/", tags=["movies"], response_model=List[Movie], status_code=200)
async def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    #data = [item for item in movies if item["category"]== category]
    db = Session()
    result = MovieService(db).get_movie_by_category(category)
    if not result:
        return JSONResponse(status_code=404, content={"message": "Categoria no encontrada"})
    #return JSONResponse(content=data,status_code=200)
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.post("/movies", tags=["movies"], response_model=dict, status_code=201)
async def create_movie(movie: Movie) -> dict:
    db = Session()
    MovieService(db).create_movie(movie)
    return JSONResponse(content={"message": "Se registró la pelicula"}, status_code=201)


@movie_router.put("/movies/{id}", tags=["movies"], response_model=dict,status_code=200)
async def update_movie(id: int, movie: Movie)-> dict:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={"message": "Pelicula no encontrada"})
    
    MovieService(db).update_movie(id, movie) 
    return JSONResponse(content={"message": "Se actualizó la pelicula"},status_code=200)

@movie_router.delete("/movies/{id}", tags=["movies"], response_model=dict, status_code=200)
async def delete_movie(id:int)-> dict:
    #for item in movies:
    #    if item["id"] == id:
    #        movies.remove(item)
    #        return JSONResponse(content={"message": "Se eliminó la pelicula"}, status_code=200)
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={"message": "Pelicula no encontrada"})

    MovieService(db).delete_movie(id)
    return JSONResponse(content={"message": "Se eliminó la pelicula"}, status_code=200)  