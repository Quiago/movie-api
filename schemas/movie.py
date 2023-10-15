from pydantic import BaseModel, Field
from typing import Optional


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(max_length=50)
    overview: str = Field(min_length=10 ,max_length=50)
    year: int = Field(default=2023, le=2023) #le == less or equal
    rating: float = Field(le=10.0, ge=1) #ge == great or equal
    category: str = Field(max_length=15)

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title":  "Mi pelicula",
                "overview": "Descripcion de la pelicula",
                "year": 2023,
                "rating": 9.8,
                "category": "Acción"
            }
        }