from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models
from .. import schemas
from ..db import get_db

router = APIRouter()

@router.get("/recipe_parameters/")
def get_recipe_parameters(db: Session = Depends(get_db)):
    parameters = db.query(models.RecipeParameter).all()
    return [
        {
            "id": param.id,
            "name": param.name,
            "type": param.type,
            "description": param.description
        } for param in parameters
    ]

@router.post("/recipe_parameters/")
def create_recipe_parameter(name: str, type: str, description: str, db: Session = Depends(get_db)):
    existing = db.query(models.RecipeParameter).filter_by(name=name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Recipe parameter with this name already exists")

    param = models.RecipeParameter(name=name, type=type, description=description)
    db.add(param)
    db.commit()
    db.refresh(param)

    return {
        "id": param.id,
        "name": param.name,
        "type": param.type,
        "description": param.description
    }

@router.delete("/recipe_parameters/{param_id}")
def delete_recipe_parameter(param_id: int, db: Session = Depends(get_db)):
    param = db.query(models.RecipeParameter).filter_by(id=param_id).first()
    if not param:
        raise HTTPException(status_code=404, detail="Parameter not found")

    db.delete(param)
    db.commit()
    return {"detail": "Deleted"}




@router.get("/recipe_parameters/by_strategy/{strategy_id}", response_model=List[schemas.RecipeParameterRead])
def get_recipe_parameters_by_strategy(strategy_id: int, db: Session = Depends(get_db)):
    # Ensure strategy exists
    strategy = db.query(models.Strategy).filter_by(id=strategy_id).first()
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")

    # Get parameter links for strategy
    links = db.query(models.StrategyRecipeParameterLink).filter_by(strategy_id=strategy_id).all()
    parameter_ids = [link.parameter_id for link in links]

    # Fetch actual parameter details
    parameters = db.query(models.RecipeParameter).filter(models.RecipeParameter.id.in_(parameter_ids)).all()

    return parameters
