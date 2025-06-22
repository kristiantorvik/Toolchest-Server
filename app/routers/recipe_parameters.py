from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas
from ..db import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()

@router.get("/recipe_parameters/")
def read_recipe_parameters(db: Session = Depends(get_db)):
    return db.query(models.RecipeParameter).all()

