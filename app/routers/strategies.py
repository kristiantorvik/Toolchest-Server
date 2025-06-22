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

@router.post("/strategies/", response_model=schemas.StrategyRead)
def create_strategy(strategy: schemas.StrategyCreate, db: Session = Depends(get_db)):
    db_strategy = models.Strategy(name=strategy.name, description=strategy.description)
    db.add(db_strategy)
    db.commit()
    db.refresh(db_strategy)

    # Create ORM-based links for recipe parameters
    for param_id in strategy.recipe_parameter_ids:
        link = models.StrategyRecipeParameterLink(
            strategy_id=db_strategy.id,
            parameter_id=param_id
        )
        db.add(link)

    db.commit()
    db.refresh(db_strategy)
    return db_strategy

@router.get("/strategies/", response_model=List[schemas.StrategyRead])
def read_strategies(db: Session = Depends(get_db)):
    return db.query(models.Strategy).all()

@router.delete("/strategies/{strategy_id}")
def delete_strategy(strategy_id: int, db: Session = Depends(get_db)):
    strategy = db.query(models.Strategy).filter(models.Strategy.id == strategy_id).first()
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    db.delete(strategy)
    db.commit()
    return {"detail": "Deleted"}

@router.get("/strategy_recipe_parameters/{strategy_id}", response_model=List[schemas.RecipeParameterRead])
def get_recipe_parameters_for_strategy(strategy_id: int, db: Session = Depends(get_db)):
    strategy = db.query(models.Strategy).filter(models.Strategy.id == strategy_id).first()
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")

    parameters = [link.parameter for link in strategy.recipe_parameter_links]
    return parameters

