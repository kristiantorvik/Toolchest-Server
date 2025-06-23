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

# ------------------------- MATERIALS -----------------------------
@router.post("/materials/", response_model=schemas.MaterialRead)
def create_material(material: schemas.MaterialCreate, db: Session = Depends(get_db)):
    db_material = models.Material(**material.dict())
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material

@router.get("/materials/", response_model=List[schemas.MaterialRead])
def read_materials(db: Session = Depends(get_db)):
    return db.query(models.Material).all()

# ------------------------- RECIPE PARAMETERS -----------------------------
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