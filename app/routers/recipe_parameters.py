from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..db import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/recipe_parameters/", response_model=schemas.RecipeParameterRead)
def create_recipe_parameter(param: schemas.RecipeParameterCreate, db: Session = Depends(get_db)):
    db_param = models.RecipeParameter(**param.dict())
    db.add(db_param)
    db.commit()
    db.refresh(db_param)
    return db_param

@router.get("/recipe_parameters/", response_model=List[schemas.RecipeParameterRead])
def read_recipe_parameters(db: Session = Depends(get_db)):
    return db.query(models.RecipeParameter).all()