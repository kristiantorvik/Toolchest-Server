from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from .. import models, schemas
from ..db import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()

@router.post("/recipes/", response_model=schemas.RecipeRead)
def create_recipe(recipe: schemas.RecipeCreate, db: Session = Depends(get_db)):
    db_recipe = models.Recipe(**recipe.dict())
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

@router.get("/recipes/", response_model=list[schemas.RecipeRead])
def read_recipes(db: Session = Depends(get_db)):
    return db.query(models.Recipe).all()

@router.delete("/recipes/{recipe_id}")
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    db.delete(recipe)
    db.commit()
    return {"detail": "Deleted"}

@router.get("/strategy_recipe_parameters/{strategy_id}", response_model=List[schemas.RecipeParameterRead])
def get_recipe_parameters_for_strategy(strategy_id: int, db: Session = Depends(get_db)):
    strategy = db.query(models.Strategy).filter(models.Strategy.id == strategy_id).first()
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")

    stmt = select(models.StrategyRecipeParameterLink).where(
        models.StrategyRecipeParameterLink.c.strategy_id == strategy_id
    )
    result = db.execute(stmt).fetchall()

    parameter_ids = [row.parameter_id for row in result]

    # DEBUG PRINT — here we see what parameter ids we fetched
    print(f"DEBUG: strategy_id={strategy_id} -> parameter_ids={parameter_ids}")

    parameters = db.query(models.RecipeParameter).filter(models.RecipeParameter.id.in_(parameter_ids)).all()

    # DEBUG PRINT — we print full parameter names/types
    for param in parameters:
        print(f"DEBUG: parameter -> id={param.id}, name={param.name}, type={param.type}")

    return parameters
